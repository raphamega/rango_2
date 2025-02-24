$("#id_cep").blur(function() {
    // Remove tudo o que não é número para fazer a pesquisa
    var cep = this.value.replace(/[^0-9]/, "");

    // Validação do CEP; caso o CEP não possua 8 números, então cancela
    // a consulta
    if (cep.length != 8) {
        return false;
    }

    // A url de pesquisa consiste no endereço do webservice + o cep que
    // o usuário informou + o tipo de retorno desejado (entre "json",
    // "jsonp", "xml", "piped" ou "querty")
    var url = "https://viacep.com.br/ws/" + cep + "/json/";

    // Faz a pesquisa do CEP, tratando o retorno com try/catch para que
    // caso ocorra algum erro (o cep pode não existir, por exemplo) a
    // usabilidade não seja afetada, assim o usuário pode continuar//
    // preenchendo os campos normalmente
    $.getJSON(url, function(dadosRetorno) {
        try {
            // Preenche os campos de acordo com o retorno da pesquisa
            $("#id_endereco").val(dadosRetorno.logradouro);
            $("#id_bairro").val(dadosRetorno.bairro);
            $("#id_municipio").val(dadosRetorno.localidade);
            $("#id_UF").val(dadosRetorno.uf);

        } catch (ex) {}
    });
});

$('#id_cnpj').remove('required');

$(function() {
    $('#id_image').change(function() {
        const file = $(this)[0].files[0];
        const fileReader = new FileReader();
        fileReader.onloadend = function() {
            $('#id_img').attr('src', fileReader.result)
        }
        fileReader.readAsDataURL(file)
    });
});

var piscando = document.getElementById('id_do_elemento');
var interval = window.setInterval(function() {
    if (piscando.style.visibility == 'hidden') {
        piscando.style.visibility = 'visible';
    } else {
        piscando.style.visibility = 'hidden';
    }
}, 5000);

function marcaDesmarca(caller) {
    var checks = document.querySelectorAll('input[type="checkbox"]');
    for (let i = 0; i < checks.length; i++) {
        checks[i].checked = checks[i] == caller;
    }
}

document.addEventListener("DOMContentLoaded", function(){
    // make it as accordion for smaller screens
    if (window.innerWidth < 992) {

      // close all inner dropdowns when parent is closed
      document.querySelectorAll('.navbar .dropdown').forEach(function(everydropdown){
        everydropdown.addEventListener('hidden.bs.dropdown', function () {
          // after dropdown is hidden, then find all submenus
            this.querySelectorAll('.submenu').forEach(function(everysubmenu){
              // hide every submenu as well
              everysubmenu.style.display = 'none';
            });
        })
      });

      document.querySelectorAll('.dropdown-menu a').forEach(function(element){
        element.addEventListener('click', function (e) {
            let nextEl = this.nextElementSibling;
            if(nextEl && nextEl.classList.contains('submenu')) {
              // prevent opening link if link needs to open dropdown
              e.preventDefault();
              if(nextEl.style.display == 'block'){
                nextEl.style.display = 'none';
              } else {
                nextEl.style.display = 'block';
              }

            }
        });
      })
    }
    // end if innerWidth
    });
    // DOMContentLoaded  end

    /* ============ desktop view ============ */
  // @media all and (min-width: 992px) {
  //   .dropdown-menu li{ position: relative; 	}
  //   .nav-item .submenu{
  //     display: none;
  //     position: absolute;
  //     left:100%; top:-7px;
  //   }
  //   .nav-item .submenu-left{
  //     right:100%; left:auto;
  //   }
  //   .dropdown-menu > li:hover{ background-color: #f1f1f1 }
  //   .dropdown-menu > li:hover > .submenu{ display: block; }
  // }
  // /* ============ desktop view .end// ============ */

  // /* ============ small devices ============ */
  // @media (max-width: 991px) {
  //   .dropdown-menu .dropdown-menu{
  //       margin-left:0.7rem; margin-right:0.7rem; margin-bottom: .5rem;
  //   }
  // }
  /* ============ small devices .end// ============ */
