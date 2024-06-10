document.addEventListener("DOMContentLoaded",function(){


document.querySelector('.show-more').addEventListener('click',function(){

    const showDescription = document.getElementById('descripcion');
    if(showDescription.style.display=='none'){
        showDescription.style.display='block';
    }else{
        showDescription.style.display = 'none';
    }
})

const AnswerButton = document.getElementById('respuestas').addEventListener('click',function(){
    const itemList = document.querySelectorAll('.barra-respuestas');

    itemList.forEach(item =>{
        if(item.style.display=='none'){
            item.style.display='block';
        }else{
            item.style.display='none';
        }
    })

})



})

