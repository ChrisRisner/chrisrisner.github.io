$( document ).ready(function() {

	/* Sidebar height set */
	$('.sidebar').css('min-height',$(document).height());

	/* Secondary contact links */
	var scontacts = $('#contact-list-secondary');
	var contact_list = $('#contact-list');
	
	scontacts.hide();
	
	contact_list.mouseenter(function(){ scontacts.fadeIn(); });
	
	contact_list.mouseleave(function(){ scontacts.fadeOut(); });

});

// Static comments
(function ($) {
	var $comments = $('.js-comments');
  
	$('#comment-form').submit(function () {
	  var form = this;
  
	  $(form).addClass('disabled');
	  $('#comment-form-submit').html('<svg class="icon spin"><use xlink:href="#icon-loading"></use></svg> Loading...');
  
	  $.ajax({
		type: $(this).attr('method'),
		url: $(this).attr('action'),
		data: $(this).serialize(),
		contentType: 'application/x-www-form-urlencoded',
		success: function (data) {
		  $('#comment-form-submit').html('Submitted');
		  $('.post__comments-form .js-notice').removeClass('notice--danger').addClass('notice--success');
		  showAlert('<strong>Thanks for your comment!</strong> It will show on the site once it has been approved.');
		},
		error: function (err) {
		  console.log(err);
		  $('#comment-form-submit').html('Submit Comment');
		  $('.post__comments-form .js-notice').removeClass('notice--success').addClass('notice--danger');
		  showAlert('<strong>Sorry, there was an error with your submission.</strong> Please make sure all required fields have been completed and try again.');
		  $(form).removeClass('disabled');
		}
	  });
  
	  return false;
	});
  
	function showAlert(message) {
	  $('.post__comments-form .js-notice').removeClass('hidden');
	  $('.post__comments-form .js-notice-text').html(message);
	}
  })(jQuery);