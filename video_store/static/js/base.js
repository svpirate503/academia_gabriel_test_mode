function openMenu(){



        const barraMovil = document.querySelector('.barra-movil');
        if(barraMovil.style.width==='0px'){
            barraMovil.style.width = '300px';
        }else{
            barraMovil.style.width = '0px';
        }





}
      
   
   function closeMenu(){


        const barraMovil = document.querySelector('.barra-movil');
        if(barraMovil.style.width==='300px'){
            barraMovil.style.width = '0px';
        }
        else{
            barraMovil.style.width = '300px';
        }




}

   