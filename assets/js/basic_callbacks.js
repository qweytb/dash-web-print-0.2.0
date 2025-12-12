// 改造console.error()以隐藏无关痛痒的警告信息
const originalConsoleError = console.error;
console.error = function (...args) {
    // 检查args中是否包含需要过滤的内容
    const shouldFilter = args.some(arg => typeof arg === 'string' && arg.includes('Warning:'));

    if (!shouldFilter) {
        originalConsoleError.apply(console, args);
    }
};


// 1. 分别定义排除元素（可单独控制）
const excludedContextMenu = []; // 允许右键菜单的元素
const excludedSelect = [];        // 允许文本选择的元素
// 允许拖拽的元素
const excludedDrag = [
    "#drag-element-transverse",
    "#drag-element-vertical",
    "#drag-element-rectangle",
    "#drag-element-text",
    "#drag-element-picture",
    "#drag-element-qrcode",
    "#drag-element-barcode",
    "#drag-element-table",
    "#drag-element-data-source-scrollbar",
];

// 2. 判断目标元素是否在排除列表中（兼容 IE）
function isExcluded(element, excludedList) {
    return excludedList.some(selector => {
        if (element.matches(selector)) return true;
        let parent = element.parentElement;
        while (parent) {
            if (parent.matches(selector)) return true;
            parent = parent.parentElement;
        }
        return false;
    });
}

// 3. 禁用右键菜单（仅排除 excludedContextMenu 中的元素）
document.addEventListener('contextmenu', function (e) {
    if (isExcluded(e.target, excludedContextMenu)) return;
    e.preventDefault();
});

// 4. 禁用文本选择（仅排除 excludedSelect 中的元素）
document.addEventListener('selectstart', function (e) {
    if (isExcluded(e.target, excludedSelect)) return;
    e.preventDefault();
});

// 5. 禁用拖拽（仅排除 excludedDrag 中的元素）
document.addEventListener('dragstart', function (e) {
    if (isExcluded(e.target, excludedDrag)) return;
    e.preventDefault();
});