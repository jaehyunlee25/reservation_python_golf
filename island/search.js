const kids = Array.from(document.getElementsByTagName('tbody')[0].children);
const result = [];
kids.forEach((tr,i) => {
  if(tr.tagName !== 'TR') return;
  if(tr.children.length < 4) return;
  result.push({
    reserved_date: tr.children[1].innerHTML,
    reserved_time: tr.children[2].innerHTML,
    reserved_course: tr.children[3].innerHTML,
  });
});
const elResult = document.createElement('div');
elResult.id = 'elResult';
elResult.innerHTML = JSON.stringify(result);
document.body.appendChild(elResult); 