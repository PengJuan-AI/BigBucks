// 引入utils.js文件
// import { searchStockByName } from '../utils.js';

const searchBox = document.getElementById('search-input')
const resultArea = document.getElementById('result-area');
const stocknameCell = resultArea.querySelector("td:first-child");
const stocksymbelCell = resultArea.querySelector("td:nth-child(2)");

const searchBtn = document.getElementById('search-btn');
searchBtn.addEventListener('click', function(event) {
    event.preventDefault();  // 阻止表单提交
    // 获取用户输入的信息
    const searchText = searchBox.value;
    // 调用searchByName方法进行搜索
    // const searchResult = searchStockByName(searchText);

    // 将搜索结果显示在界面上
    stocknameCell.innerHTML = searchText;
});