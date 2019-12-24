
$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $(".modal-config .modal-content").html("");
          $(".modal-config").modal("show");
        },
        success: function (data) {
          $(".modal-config .modal-content").html(data.form_html);
        }
      });
    };
  
    var saveForm = function () {
		var form = $(this);
		var formData = new FormData(this);
		var msg_succes;
		var msg_error;
		var clear = false;

		if (form.attr("id") == "palestrante-create"){
			msg_succes = 'Palestrante adicionada com sucessor!';
			msg_error = 'Não foi possivel adicionar o palestrante';
			clear = true;
		
		}else if (form.attr("id") == "palestrante-update"){
			msg_succes = 'Palestrante alterada com sucessor!';
			msg_error = 'Não foi possivel alterar o palestrante';
		
		}else{
			msg_succes = 'Palestrante excluída com sucessor!';
			msg_error = 'Não foi possivel excluir o palestrante';
		}
		
		$.ajax({
			url: form.attr("action"),
			type: form.attr("method"),
			data: formData,
			cache: false,
			processData: false,
    		contentType: false,
			success: function (data) {
				if (data.valido_form){
					$("#palestrante-table tbody").html(data.table_html)
					$("#update-create").html(data.programacao_create_html)
					$("#programacao-table tbody").html(data.table_programacao_html)
					$(".modal-config").modal("hide");
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
				}
				else{
					$(".modal-config").modal("hide");
					$.notify({
						// optionse
						message: msg_error,
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
				}
			}

		});

		if(clear)
			$("#palestrante-create")[0].reset();

		return false;
    };
  
    /* Binding */
  
    // Create Programação
	$("#palestrante-create").submit(saveForm);

	//Update Programação
	$("#palestrante-table").on("click", ".palestrante-update-form", loadForm);
    $(".modal-config").on("submit", "#palestrante-update", saveForm);

    // Delete Programação
    $("#palestrante-table").on("click", ".palestrante-delete-form", loadForm);
    $(".modal-config").on("submit", "#palestrante-delete", saveForm);
  
  });
