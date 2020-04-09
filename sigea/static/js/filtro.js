$(function () {

    var filtroForm = function () {
		var form = $(this);
		
		$.ajax({
			url: form.attr("action"),
			data: form.serialize(),
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				$("#inscricoes-table").html(data.tabela_filtro)
				$("#total-inscricao").html(data.total_inscricao)
				$("#gera-pdf").html(data.buttao_gera_pdf)
			},
		});
		return false;
    };
  
    /* Binding */
  
    // Create Programação
	$("#filtro-form").submit(filtroForm);
  });

  