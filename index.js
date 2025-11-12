let box =document.querySelectorAll('.box');
const text =document.querySelectorAll('.text');

box.forEach((a,index)=>{
            a.addEventListener('click', function(){
                box.forEach((c)=>{
                    c.classList.remove('color');
                })
                a.classList.add('color');
                text.forEach((b)=>{
                    b.classList.remove('active');
                })
                text[index].classList.add('active');
            })
        })