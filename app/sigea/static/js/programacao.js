$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $(".modal-organizador .modal-content").html("");
          $(".modal-organizador").modal("show");
        },
        success: function (data) {
          $(".modal-organizador .modal-content").html(data.form_html);
        }
      });
    };
  
    var saveForm = function () {
		var form = $(this);
		var msg_succes;
		var msg_error;
		var clear = false;

		if (form.attr("id") == "programacao-create"){
			msg_succes = 'Programação adicionada com sucessor!';
			msg_error = 'Não foi possivel adicionar a programação!';
			clear = true;
		
		}else if (form.attr("id") == "programacao-update"){
			msg_succes = 'Programação alterada com sucessor!';
			msg_error = 'Não foi possivel alterar a programação!';
		
		}else{
			msg_succes = 'Programação excluída com sucessor!';
			msg_error = 'Não foi possivel excluir a programação!';
		}
		
		$.ajax({
			url: form.attr("action"),
			data: form.serialize(),
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				$("#programacao-table tbody").html(data.table_html)
				$(".modal-organizador").modal("hide");
				$.notify({
					// options
					message: msg_succes,
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
					message: msg_error,
					},{
					// settings
					type: 'warning',

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

		if(clear)
			$("#programacao-create")[0].reset();

		return false;
    };
  
    /* Binding */
  
    // Create Programação
	$("#programacao-create").submit(saveForm);

	//Update Programação
	$("#programacao-table").on("click", ".programacao-update-form", loadForm);
    $(".modal-organizador").on("submit", "#programacao-update", saveForm);

    // Delete Programação
    $("#programacao-table").on("click", ".programacao-delete-form", loadForm);
    $(".modal-organizador").on("submit", "#programacao-delete", saveForm);
  
  });