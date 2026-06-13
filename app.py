import csv
import os
from flask import Flask, render_template, request, abort, jsonify

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sentinel_demo_inventory_100_products.csv')


def load_products():
    products = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            row['price_mxn'] = int(row['price_mxn'])
            row['stock'] = int(row['stock'])
            products.append(row)
    return products


products = load_products()
categories = sorted(set(p['category'] for p in products))


def get_products(category=None, search=None):
    result = products
    if category and category != 'all':
        result = [p for p in result if p['category'] == category]
    if search:
        q = search.lower()
        result = [p for p in result if q in p['name'].lower() or q in p['sku'].lower() or q in p['brand'].lower()]
    return result


@app.template_filter('mxn')
def format_mxn(value):
    return f"${value:,} MXN"


VALID_BROWSERS = ('chrome', 'firefox', 'safari', 'edge', 'opera', 'mozilla')


def is_valid_ua(ua):
    if not ua:
        return False
    ua_lower = ua.lower()
    return any(b in ua_lower for b in VALID_BROWSERS)


@app.before_request
def guard_middleware():
    if request.path.startswith('/guard'):
        ua = request.headers.get('User-Agent', '')
        if not is_valid_ua(ua):
            abort(403)
        if not request.headers.get('Accept'):
            abort(403)
        if not request.headers.get('Accept-Language'):
            abort(403)


@app.route('/')
def index():
    return render_template('index.html', categories=categories)


def _list_view(prefix):
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12

    filtered = get_products(category, search)
    total = len(filtered)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    page_products = filtered[start:start + per_page]

    return render_template('store.html',
        prefix=prefix,
        products=page_products,
        total=total,
        categories=categories,
        current_category=category,
        search=search,
        page=page,
        total_pages=total_pages,
    )


def _detail_view(prefix, sku):
    product = next((p for p in products if p['sku'] == sku), None)
    if not product:
        abort(404)
    return render_template('product.html', product=product, prefix=prefix)


@app.route('/simple/')
def simple_list():
    return _list_view('/simple')


@app.route('/simple/product/<sku>')
def simple_detail(sku):
    return _detail_view('/simple', sku)


@app.route('/guard/')
def guard_list():
    return _list_view('/guard')


@app.route('/guard/product/<sku>')
def guard_detail(sku):
    return _detail_view('/guard', sku)


@app.route('/dynamic/')
def dynamic_shell():
    return render_template('dynamic.html')


@app.route('/dynamic/api/products')
def dynamic_api():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    return jsonify(get_products(category, search))


@app.route('/dynamic/product/<sku>')
def dynamic_detail(sku):
    return _detail_view('/dynamic', sku)


if __name__ == '__main__':
    app.run(debug=True, port=5100)
