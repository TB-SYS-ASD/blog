// 1. 主题切换（昼夜按钮）
const btn = document.getElementById('themeToggle');
const html = document.documentElement;
const cacheKey = 'theme';

// 初始化
const pre = localStorage.getItem(cacheKey) || 'dark';
html.setAttribute('data-theme', pre === 'light' ? 'light' : 'dark');
btn.textContent = pre === 'light' ? '夜' : '昼';

btn.addEventListener('click', () => {
  const cur = html.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem(cacheKey, next);
  btn.textContent = next === 'dark' ? '昼' : '夜';
});

// 2. 文章索引（空数组先占位，避免报错）
let index = [];

// 3. 渲染函数
function render(arr) {
  const list = document.getElementById('postList');
  list.innerHTML = arr.map(o => `
    <li>
      <a href="posts/${o.file}">${o.title}</a>
      <time>${o.date}</time>
    </li>`).join('');
}

// 4. 异步加载索引
fetch('posts/index.json')
  .then(res => res.json())
  .then(data => {
    index = data;
    render(index); // 首屏渲染
  })
  .catch(err => console.error('加载文章索引失败', err));

// 5. 搜索框实时过滤
document.getElementById('searchBox').addEventListener('input', e => {
  const kw = e.target.value.trim().toLowerCase();
  const fil = index.filter(o => o.title.toLowerCase().includes(kw));
  render(fil);
});