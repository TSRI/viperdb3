$(function(){
  var $container = $('#container');

  $container.isotope({
    filter: '.virus'
  });

  $('#container').isotope({ layoutMode : 'fitRows' });

  $('#filters a').click(function(){
    var selector = $(this).attr('data-filter');
    $container.isotope({filter:selector});
    return false;
  })
});
