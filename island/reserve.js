const REPORT = document.createElement('input');
REPORT.type = 'hidden';
REPORT.id = 'REPORT';
document.body.appendChild(REPORT);

const year = '${year}';
const month = '${month}';
const date = '${date}';
const time = '${time}';
const course = '${course}';
const fulldate = year + month + date;
const times = Array.from(document.getElementById('res_step2').getElementsByTagName('a'));
let SEL_ITEM;
times.forEach((el) => {
  if(el.href.indexOf(fulldate) === -1) return;
  if(el.href.indexOf(time) === -1) return;
  if(el.href.indexOf(course) === -1) return;
  SEL_ITEM = el;
});
if(!SEL_ITEM) {
  REPORT.value = false;
} else {
  SEL_ITEM.click();
}