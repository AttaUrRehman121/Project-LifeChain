$(document).ready(function(){
    $('.fa-bars').click(function(){
        $(this).toggleClass('fa-times');
        $('.navbar').toggleClass('nav-toggle');
    });
    $(Window).on('scroll load',function(){
        $('.fa-bars').removeClass('fa-times');
        $('.navbar').removeClass('nav-toggle');
        
        if($(Window).scrollTop()>30){
            $('header').addClass('header-active');
        }
        else{
            $('header').removeClass('header-active');
        }
    })
});