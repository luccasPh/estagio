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
				$("#banner-form").html(data.banner_form);
				$("#escodidas").html(data.escodidas);
				$("#capa-form").html(data.capa_form);
				$("#titulo-nav").html(data.titulo_nav);
				$.notify({
					// options
					message: "Configuração do evento salvo com sucesso!",
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
				$.notify({
					// optionse
					message: "Não possivel salva as configuração do evento!",
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
  
    // Create Programação
	$("#inicio-form").submit(saveForm);
	$("#capa-form").submit(saveForm);

  });
