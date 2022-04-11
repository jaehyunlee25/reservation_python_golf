const inputs = document.getElementsByTagName('input');
const ipts = [];
Array.from(inputs).forEach((input) => {
    if(input.type === 'hidden') return;
    if(input.type === 'checkbox') return;
    ipts.push(input);
});
ipts[0].value = '${login_id}';
ipts[1].value = '${login_password}';

const btns = document.getElementsByClassName('login');
Array.from(btns).forEach((btn) => {
    if(btn.tagName === 'A') return;
    btn.click();
});