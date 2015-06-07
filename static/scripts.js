// Caching selector to optimize performance & scalability
var tabs =  $('.nav-tabs');

$('.tab').hide();

tabs.find('a').on('click', function(e){
	e.preventDefault();
	// Hides all insctive tabs to achieve the tabbing effect
	tabs.find('.active').removeClass('active');
	$(this).addClass('active');

	var newTab = $(this.hash);
	var newHeight = newTab.height();
	var container = $('.panels');

	// Fades out the previous tab that was showing
	newTab.siblings(':visible').fadeOut(300);
	container.animate({'height': newHeight}, 600, function(){
		newTab.fadeIn('fast');
	});

}).first().click();