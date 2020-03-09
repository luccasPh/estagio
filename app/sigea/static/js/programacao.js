$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'GET',
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
		var clear = false;
		
		$.ajax({
			url: form.attr("action"),
			data: form.serialize(),
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				if (data.valido_form){
					$("#programacao-table tbody").html(data.table_html);
					$(".modal-config").modal("hide");
					$("#area-filtro").html(data.filtro_form);
					$("#messagens").html(data.messages)
				}
				else{
					$(".modal-config").modal("hide");
					$("#messagens").html(data.messages)
				}
			}	

		});
		$("#programacao-create")[0].reset();

		return false;
    };
  
    /* Binding */
  
    // Create Programação
	$("#programacao-create").submit(saveForm);

	//Update Programação
	$("#programacao-table").on("click", ".programacao-update-form", loadForm);
    $(".modal-config").on("submit", "#programacao-update", saveForm);

    // Delete Programação
    $("#programacao-table").on("click", ".programacao-delete-form", loadForm);
    $(".modal-config").on("submit", "#programacao-delete", saveForm);
  
  });