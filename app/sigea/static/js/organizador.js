$('#myList a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
  })

$(function () {
	$('#datetimepicker1').datetimepicker({
		format: 'L',
		locale: 'pt-BR',
		minDate:new Date()
	});

	$('#datetimepicker2').datetimepicker({
		format: 'L',
		locale: 'pt-BR',
		minDate:new Date()
	});

	$('#datetimepicker3').datetimepicker({
		locale: 'pt-BR',
		fromat: 'LTS',
		
	});

	$('#datetimepicker4').datetimepicker({
		locale: 'pt-BR',
		fromat: 'LTS',
		
	});
	
});


$("#menu-toggle").click(function(e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

function bs_input_file() {
	$(".input-file").before(
		function() {
			if ( ! $(this).prev().hasClass('input-ghost') ) {
				var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
				element.attr("name",$(this).attr("name"));
				element.change(function(){
					element.next(element).find('input').val((element.val()).split('\\').pop());
				});
				$(this).find("button.btn-choose").click(function(){
					element.click();
				});
				$(this).find("button.btn-reset").click(function(){
					element.val(null);
					$(this).parents(".input-file").find('input').val('');
				});
				$(this).find('input').css("cursor","pointer");
				$(this).find('input').mousedown(function() {
					$(this).parents('.input-file').prev().click();
					return false;
				});
				return element;
			}
		}
	);
}
$(function() {
	bs_input_file();
});

$(function () {
  $('[data-toggle="popover"]').popover()
})
