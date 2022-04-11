const kids = Array.from(document.getElementById('tbody-reservation').children);
const result = [];
kids.forEach((tr,i) => {
  if(tr.tagName !== 'TR') return;
  result.push({
    reserved_date: tr.children[0].innerHTML,
    reserved_time: tr.children[1].innerHTML,
    reserved_course: tr.children[2].innerHTML,
  });
});
const elResult = document.createElement('div');
elResult.id = 'elResult';
elResult.innerHTML = JSON.stringify(result);
document.body.appendChild(elResult); 