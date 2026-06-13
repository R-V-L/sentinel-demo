const CATEGORIES = ['GPU', 'CPU', 'SSD', 'RAM', 'MONITOR'];
const PER_PAGE = 12;

let allProducts = [];
let currentCategory = 'all';
let currentSearch = '';
let currentPage = 1;

async function loadProducts() {
    const params = new URLSearchParams();
    if (currentCategory !== 'all') params.set('category', currentCategory);
    if (currentSearch) params.set('search', currentSearch);

    try {
        const resp = await fetch('/dynamic/api/products?' + params);
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        allProducts = await resp.json();
        currentPage = 1;
        render();
    } catch (e) {
        document.getElementById('product-grid').innerHTML =
            '<p class="text-red-400 col-span-full text-center py-12">Error al cargar productos.</p>';
    }
}

function render() {
    renderCategoryTabs();
    renderGrid();
    renderPagination();
    document.getElementById('clear-btn').classList.toggle('hidden', !currentSearch);
    document.getElementById('result-count').textContent = allProducts.length + ' productos';
}

function renderCategoryTabs() {
    const container = document.getElementById('category-tabs');
    let html = '<button onclick="setCategory(\'all\')" class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors ' +
        (currentCategory === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600') +
        '">Todo</button>';
    CATEGORIES.forEach(cat => {
        html += '<button onclick="setCategory(\'' + cat + '\')" class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors ' +
            (currentCategory === cat ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600') +
            '">' + cat + '</button>';
    });
    container.innerHTML = html;
}

function renderGrid() {
    const totalPages = Math.ceil(allProducts.length / PER_PAGE) || 1;
    if (currentPage > totalPages) currentPage = totalPages;
    const start = (currentPage - 1) * PER_PAGE;
    const pageProducts = allProducts.slice(start, start + PER_PAGE);

    const grid = document.getElementById('product-grid');
    if (pageProducts.length === 0) {
        grid.innerHTML = '<p class="text-gray-400 col-span-full text-center py-12">No se encontraron productos.</p>';
        return;
    }

    grid.innerHTML = pageProducts.map(p =>
        '<a href="/dynamic/product/' + p.sku + '"' +
        ' class="group bg-gray-800 rounded-xl border border-gray-700 hover:border-blue-500 transition-all hover:shadow-lg hover:shadow-blue-500/5 overflow-hidden">' +
        '<div class="p-5">' +
        '<div class="flex items-center justify-between mb-3">' +
        '<span class="text-xs font-medium text-gray-400 uppercase tracking-wider">' + p.brand + '</span>' +
        '<span class="text-xs px-2 py-0.5 rounded-full font-medium ' + (p.stock > 0 ? 'bg-green-900/50 text-green-400' : 'bg-red-900/50 text-red-400') + '">' +
        (p.stock > 0 ? 'En stock' : 'Agotado') + '</span>' +
        '</div>' +
        '<h3 class="text-base font-semibold text-white group-hover:text-blue-400 transition-colors leading-snug">' + p.name + '</h3>' +
        '<p class="text-xs text-gray-500 mt-1 mb-3">' + p.category + ' &middot; SKU: ' + p.sku + '</p>' +
        '<p class="text-xl font-bold text-white">$' + p.price_mxn.toLocaleString() + ' MXN</p>' +
        '</div>' +
        '</a>'
    ).join('');
}

function renderPagination() {
    const totalPages = Math.ceil(allProducts.length / PER_PAGE) || 1;
    const container = document.getElementById('pagination');
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = '';
    if (currentPage > 1) {
        html += '<button onclick="goToPage(' + (currentPage - 1) + ')" class="px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition-colors">&larr; Ant</button>';
    }

    for (let i = 1; i <= totalPages; i++) {
        if (i <= 3 || i > totalPages - 3 || (i >= currentPage - 1 && i <= currentPage + 1)) {
            html += (i === currentPage)
                ? '<span class="px-3 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium">' + i + '</span>'
                : '<button onclick="goToPage(' + i + ')" class="px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition-colors">' + i + '</button>';
        } else if (i === 4 || i === totalPages - 3) {
            html += '<span class="px-2 py-2 text-gray-500 text-sm">&hellip;</span>';
        }
    }

    if (currentPage < totalPages) {
        html += '<button onclick="goToPage(' + (currentPage + 1) + ')" class="px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition-colors">Sig &rarr;</button>';
    }

    container.innerHTML = html;
}

function setCategory(cat) {
    currentCategory = cat;
    loadProducts();
}

function doSearch() {
    currentSearch = document.getElementById('search-input').value;
    loadProducts();
}

function clearSearch() {
    currentSearch = '';
    document.getElementById('search-input').value = '';
    loadProducts();
}

function goToPage(page) {
    currentPage = page;
    renderGrid();
    renderPagination();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('search-input').addEventListener('keydown', function (e) {
        if (e.key === 'Enter') doSearch();
    });
    loadProducts();
});
