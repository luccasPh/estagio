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
          $(".modal-index .modal-content").html("");
          $(".modal-index").modal("show");
        },
        success: function (data) {
          $(".modal-index .modal-content").html(data.form_html);
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
				$(".modal-index").modal("hide");
				$("#messagens").html(data.messages)
			}
		});

		return false;
    };
  
	// Editar Organização
	$("#editar-organizacao").on("click", loadForm)
	$(".modal-index").on("submit", "#organizacao-update", saveForm);

	// Delete Programação
	$("#card-eventos").on("click", ".evento-delete", loadForm);
    $(".modal-index").on("submit", "#evento-delete", saveForm);
  
  });
