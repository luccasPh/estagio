$(function () {

	$('#datetimepicker3').datetimepicker({
		format: 'L',
		locale: 'pt-BR',
		minDate: moment().startOf('day') 
	});

	$('#datetimepicker4').datetimepicker({
		format: 'L',
		locale: 'pt-BR',
		minDate: moment().startOf('day')
	});
	
  });

$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $(".modal-evento .modal-content").html("");
          $(".modal-evento").modal("show");
        },
        success: function (data) {
          $(".modal-evento .modal-content").html(data.form_html);
        }
      });
    };
  
    var saveForm = function () {
		var form = $(this);

		$.ajax({
			url: form.attr("action"),
			data: form.serialize(),
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				$("#card-eventos").html(data.evento_cards)
				$(".modal-evento").modal("hide");
				$.notify({
					// options
					message: "Evento excluída com sucessor!",
					},{
					// settings
					type: 'success',
					timer: 500,
					placement: {
						from: "top",
						align: "center"
					},

					animate: {
						enter: 'animated bounceInDown',
						exit: 'animated bounceOutUp'
					},
				});
			},
			error: function() {
				$(".modal-organizador").modal("hide");
				$.notify({
					// optionse
					message: "Não foi possivel excluir o evento",
					},{
					// settings
					type: 'danger',

					placement: {
						from: "top",
						align: "center"
					},

					animate: {
						enter: 'animated bounceInDown',
							exit: 'animated bounceOutUp'
					},
				});
			},

		});

		return false;
    };
  
    /* Binding */

	// Delete Programação
	$("#card-eventos").on("click", ".evento-confirm", loadForm);
    $(".modal-evento").on("submit", "#evento-delete", saveForm);
  
  });