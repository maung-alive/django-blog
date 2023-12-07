/* const cursor = document.querySelector('.cursor');


const positionElement = (e)=> {
  const mouseY = e.clientY;
  const mouseX = e.clientX;

  cursor.style.top = mouseY + 'px';
  cursor.style.left = mouseX + 'px';
 
}

window.addEventListener('mousemove', -positionElement) */
const navStyle = (e) => {
  if (document.documentElement.scrollTop > 200) {
    document.querySelector("#home-nav").style.backgroundColor = "rgba(200,200,200,0.8)";
    document.querySelector("#home-nav").style.color = "black";
  }
  else {
    document.querySelector("#home-nav").style.backgroundColor = "rgb(15, 23, 42)";
    document.querySelector("#home-nav").style.color = "white";
  }
}

window.addEventListener("scroll", navStyle)

function showModal (catName) {
  $("#modal").toggleClass("hidden");
  $("#modal #category-name").text(catName);
  $("#modal #article").attr('data-category', catName);
}

function setCategory (e, article) {
  $.get(`?type=add&cat=${$(e).attr('data-category')}&title=${article}`, function (data) {})
  $(e).addClass('bg-green-100')
}

function addNewCat(e) {
  $.get(`?type=add&cat=${$('#catName').val()}`, function (data) {})
}