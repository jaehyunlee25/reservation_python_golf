const inputs = document.getElementsByTagName('input');
const ipts = [];
Array.from(inputs).forEach((input) => {
    if(input.type === 'hidden') return;
    ipts.push(input);
});
ipts[0].value = '${login_id}';
ipts[1].value = '${login_password}';

Data_Save();