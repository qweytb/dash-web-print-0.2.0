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
    "#drag-element-transverse",  // 横线
    "#drag-element-vertical",  // 竖线
    "#drag-element-rectangle", // 矩形
    "#drag-element-text",  // 文本
    "#drag-element-picture", // 图片
    "#drag-element-qrcode", // 二维码
    "#drag-element-barcode", // 条形码
    "#drag-element-table",  // 表格
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


// 鼠标上面的鼠标移动时，生成一个“横线”的拖拽图

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. 横线函数 ---
    function createLineImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 120;
        canvas.height = 30;
        ctx.beginPath();
        ctx.moveTo(10, 15);
        ctx.lineTo(110, 15);
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#000000';
        ctx.stroke();
        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 2. 竖线函数 ---
    function createVerticalImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 30;
        canvas.height = 120;
        ctx.beginPath();
        ctx.moveTo(15, 10);
        ctx.lineTo(15, 110);
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#000000';
        ctx.stroke();
        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 3. 矩形函数 ---
    function createRectImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 100;
        canvas.height = 100;
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#000000';
        ctx.strokeRect(10, 10, 80, 80);
        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 4. 文字布局函数 ---
    function createTextImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 100;
        canvas.height = 40;
        ctx.setLineDash([5, 3]);
        ctx.lineWidth = 1;
        ctx.strokeStyle = '#555555';
        ctx.strokeRect(10, 10, 80, 26);
        ctx.font = 'bold 20px Arial';
        ctx.fillStyle = '#555555';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('T', 50, 20);
        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 5. 图片布局函数 ---
    function createImageImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 100;
        canvas.height = 100;
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#000000';
        ctx.strokeRect(10, 10, 80, 40);
        ctx.beginPath();
        ctx.moveTo(25, 40);
        ctx.lineTo(50, 20);
        ctx.lineTo(75, 40);
        ctx.closePath();
        ctx.fillStyle = '#cccccc';
        ctx.fill();
        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 6. 二维码函数 (新增) ---
    function createQRImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 80;
        canvas.height = 80;

        // 画外框
        ctx.lineWidth = 1;
        ctx.strokeStyle = '#000000';
        ctx.strokeRect(5, 5, 70, 70);

        // 画三个角的回字 (模拟二维码定位点)
        // 左上
        ctx.fillRect(10, 10, 20, 20);
        ctx.clearRect(15, 15, 10, 10);
        ctx.fillRect(17, 17, 6, 6);

        // 右上
        ctx.fillRect(50, 10, 20, 20);
        ctx.clearRect(55, 15, 10, 10);
        ctx.fillRect(57, 17, 6, 6);

        // 左下
        ctx.fillRect(10, 50, 20, 20);
        ctx.clearRect(15, 55, 10, 10);
        ctx.fillRect(17, 57, 6, 6);

        // 随便画几个点模拟数据
        ctx.fillRect(40, 40, 5, 5);
        ctx.fillRect(50, 50, 5, 5);
        ctx.fillRect(60, 40, 5, 5);

        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 7. 条形码函数 (新增) ---
    function createBarcodeImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 120;
        canvas.height = 50;

        // 画几条粗细不一的竖线模拟条形码
        ctx.fillStyle = '#000000';
        let x = 10;
        // 简单的循环画线
        for (let i = 0; i < 15; i++) {
            let width = Math.random() > 0.5 ? 2 : 4; // 随机宽度
            ctx.fillRect(x, 5, width, 30);
            x += width + 2; // 间距
        }

        // 底部数字模拟
        ctx.font = '10px Arial';
        ctx.fillText('12345678910', 10, 45);

        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 8. 表格函数 (新增) ---
    function createTableImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 100;
        canvas.height = 60;

        ctx.lineWidth = 1;
        ctx.strokeStyle = '#000000';

        // 外框
        ctx.strokeRect(10, 10, 80, 40);

        // 中间横线 (两行)
        ctx.beginPath();
        ctx.moveTo(10, 23);
        ctx.lineTo(90, 23);
        ctx.moveTo(10, 36);
        ctx.lineTo(90, 36);
        ctx.stroke();

        // 中间竖线 (两列)
        ctx.beginPath();
        ctx.moveTo(36, 10);
        ctx.lineTo(36, 50);
        ctx.moveTo(63, 10);
        ctx.lineTo(63, 50);
        ctx.stroke();

        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }
    // --- 8.5 抓取手势函数 (新增) ---
    function createHandImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 32;
        canvas.height = 32;

        // 画一个简单的抓取手势 (一个拳头)
        ctx.fillStyle = '#000000'; // 黑色手

        // 手掌主体
        ctx.beginPath();
        ctx.arc(16, 16, 10, 0, Math.PI * 2);
        ctx.fill();

        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    // --- 9. 提前准备好所有图片 ---
    const horizontalDragImg = createLineImage(); // 横线
    const verticalDragImg = createVerticalImage(); // 竖线
    const rectDragImg = createRectImage(); // 矩形
    const textDragImg = createTextImage();  // 文字
    const imageDragImg = createImageImage(); // 图片
    const qrDragImg = createQRImage();        // 二维码
    const barcodeDragImg = createBarcodeImage(); // 条形码
    const tableDragImg = createTableImage();   //  表格
    const handDragImg = createHandImage(); //  抓取手势

    // --- 10. 监听拖拽 ---
    document.addEventListener('dragstart', function (event) {
        const target = event.target;

        // 抓取手势
        event.dataTransfer.setDragImage(handDragImg, 10, 10);

        // 1. 强制设置 document.body 的 cursor 为 grabbing (抓住的手)
        // 这是最有效的一招，作用范围最大
        document.body.style.cursor = 'grabbing';

        // 2. 尝试设置 dataTransfer 的效果（虽然不改图标，但有时能辅助状态）
        event.dataTransfer.effectAllowed = 'copyMove';

        // 拖拽图片
        if (target.id === 'drag-element-transverse') {
            event.dataTransfer.setDragImage(horizontalDragImg, 60, 15);
        }
        else if (target.id === 'drag-element-vertical') {
            event.dataTransfer.setDragImage(verticalDragImg, 15, 60);
        }
        else if (target.id === 'drag-element-rectangle') {
            event.dataTransfer.setDragImage(rectDragImg, 50, 30);
        }
        else if (target.id === 'drag-element-text') {
            event.dataTransfer.setDragImage(textDragImg, 50, 20);
        }
        else if (target.id === 'drag-element-picture') {
            event.dataTransfer.setDragImage(imageDragImg, 50, 30);
        }
        else if (target.id === 'drag-element-qrcode') { // 新增
            event.dataTransfer.setDragImage(qrDragImg, 40, 40);
        }
        else if (target.id === 'drag-element-barcode') { // 新增
            event.dataTransfer.setDragImage(barcodeDragImg, 60, 25);
        }
        else if (target.id === 'drag-element-table') { // 新增
            event.dataTransfer.setDragImage(tableDragImg, 50, 30);
        }
        // 2. 读取 data-type 属性
        // 即使 ID 千变万化，只要 data-type 一样，我们就能识别
        const type = target.getAttribute('data-type');
        if (type === 'text') {
            event.dataTransfer.setDragImage(textDragImg, 30, 20);
        }
    });
    // --- 11. 监听拖拽结束 ---
    document.addEventListener('dragend', function (event) {
        // 松开后，恢复 body 的样式为默认（箭头）
        document.body.style.cursor = 'default';

        const target = event.target;
        // 恢复组件本身的样式为 grab（张开的手），准备下次抓取
        if (target) target.style.cursor = 'grab';
    });
});