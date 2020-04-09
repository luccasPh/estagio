$(function () {
	$('#datetimepicker1').datetimepicker({
		format: 'L',
		locale: 'pt-BR',
		minDate: moment().startOf('day')
	});

	$('#datetimepicker2').datetimepicker({
		format: 'L',
		locale: 'pt-BR',
		minDate: moment().startOf('day')
	});

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

	$('#datetimepicker5').datetimepicker({
		locale: 'pt-BR',
		minDate: moment().startOf('day')
	});
	$('#datetimepicker6').datetimepicker({
		locale: 'pt-BR',
		minDate: moment().startOf('day')
	});
	
});


$("#menu-toggle").click(function(e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});


$(function () {

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
		
		$.ajax({
			url: form.attr("action"),
			type: form.attr("method"),
			data: formData,
			cache: false,
			processData: false,
			contentType: false,
			dataType: 'json',
			success: function (data) {
				$(".modal-config").modal("hide");
				$("#banner-form").html(data.banner_form);
				$("#escodidas").html(data.escodidas);
				$("#capa-form").html(data.capa_form);
				$("#titulo-nav").html(data.titulo_nav);
				$("#messagens").html(data.messages)
			},

		});
		return false;
    };
  
	//Editar Organizacao
	$("#editar-organizacao").on("click", loadForm)
	$(".modal-config").on("submit", "#organizacao-update", saveForm);
  
    // Create Programação
	$("#inicio-form").submit(saveForm);
	$("#apresentacao-form").submit(saveForm);

  });
