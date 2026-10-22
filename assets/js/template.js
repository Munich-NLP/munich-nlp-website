// Keep the calendar's scripts out of the initial page render. Templates stay
// inert until the page has painted and the calendar enters the viewport.
(function () {
	var templates = document.querySelectorAll('.luma-calendar-template');
	if (!templates.length) return;

	function showCalendar(container) {
		var template = container.querySelector('.luma-calendar-template');
		if (!template) return;
		container.appendChild(template.content.cloneNode(true));
		template.remove();
	}

	function observeCalendars() {
		if (!('IntersectionObserver' in window)) {
			templates.forEach(function (template) { showCalendar(template.parentElement); });
			return;
		}
		var observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				showCalendar(entry.target);
				observer.unobserve(entry.target);
			});
		});
		templates.forEach(function (template) { observer.observe(template.parentElement); });
	}

	function afterPageLoad() {
		requestAnimationFrame(function () { requestAnimationFrame(observeCalendars); });
	}
	if (document.readyState === 'complete') afterPageLoad();
	else window.addEventListener('load', afterPageLoad, { once: true });
})();

jQuery(document).ready(function ($) {
	if ($.fn.carousel && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
		$('.carousel').carousel('pause');
	}

	var my_nav = $('.navbar-sticky');
	// grab the initial top offset of the navigation 
	var sticky_navigation_offset_top = my_nav.length ? my_nav.offset().top : 0;

	// our function that decides weather the navigation bar should have "fixed" css position or not.
	var sticky_navigation = function () {
		if (!my_nav.length) return;
		var scroll_top = $(window).scrollTop(); // our current vertical position from the top

		// if we've scrolled more than the navigation, change its position to fixed to stick to top, otherwise change it back to relative
		if (scroll_top > sticky_navigation_offset_top) {
			my_nav.addClass('stick');
		} else {
			my_nav.removeClass('stick');
		}
	};

	var initio_parallax_animation = function () {
		if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
		$('.parallax').each(function (i, obj) {
			var speed = $(this).data('parallax-speed');
			if (speed) {
				var background_pos = '-' + (window.pageYOffset / speed) + "px";
				$(this).css('background-position', 'center ' + background_pos);
			}
		});
	}

	// run our function on load
	sticky_navigation();

	// and run it again every time you scroll
	$(window).scroll(function () {
		sticky_navigation();
		initio_parallax_animation();
	});

});
