const REPORT = document.createElement('input');
REPORT.type = 'hidden';
REPORT.id = 'REPORT';
document.body.appendChild(REPORT);

const year = '${year}';
const month = '${month}';
const date = '${date}';
const time = '${time}';
const course = '${course}';
const fulldate = year + '.' + month + '.' + date;

const kids = Array.from(document.getElementById('tbody-reservation').children);
let SEL_ITEM;
kids.forEach((tr,i) => {
  if(tr.children.length < 6) return;
  const tds = tr.children;
  const tdFullDate = tds[0].innerHTML;
  const tdTime = tds[1].innerHTML.replace(':', '');
  const tdCourse = tds[2].innerHTML;
  const btnCancel = tds[5].children[0];
  if(tdFullDate != fulldate || tdTime != time || tdCourse != course) return;
  SEL_ITEM = btnCancel;
  btnCancel.id = 'SEL_BUTTON';
});
if(!SEL_ITEM) {
  REPORT.value = false;
}