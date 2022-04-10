const REPORT = document.createElement('input');
REPORT.type = 'hidden';
REPORT.id = 'REPORT';
document.body.appendChild(REPORT);

const year = '${year}';
const month = '${month}';
const date = '${date}';
const time = '${time}';
const course = '${course}';
const dict_course = {'EAST': 1, 'SOUTH': 2, 'WEST':3}

String.prototype.getParams = function(){
  const re = /JavaScript:Confirm_Book\((.+)\)/;
  const str = re.exec(this)[1];
  const str2 = str.replace(/\'/g, '');
  const result = str2.split(',');
  return {
    fulldate: result[0],
    course: result[1],
    time: result[2],
  };
};
const kids = Array.from(document.getElementsByTagName('tbody')[0].getElementsByTagName('button'));
let SEL_ITEM;
kids.forEach((btn,i) => {
  const params = btn.getAttribute('onclick').getParams();
  if(params.fulldate != year + "" + month + "" + date || params.time != time || params.course != dict_course[course]) return;
  SEL_ITEM = btn;
  btn.id = 'SEL_BUTTON';
});
if(!SEL_ITEM) {
  REPORT.value = false;
}