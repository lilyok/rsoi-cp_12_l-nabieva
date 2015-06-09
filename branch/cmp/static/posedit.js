'use strict';
  
var univ = new Array();
var lang = new Array();
var llev = new Array();
var trip = new Array();
var sphere = new Array();
var schedule = new Array();

var isLoad = false;
var isLoadAbout = false;

var getAbout = function() { 
    if (!isLoadAbout){
        $.get( '/position/getAbout' ).success( function(about) {
            $('#fdate').datepicker('setDate',String(about.data));
            $('#info').val(about.about);
            isLoadAbout = true;               
        }).error( function() {
            alert( 'Error: try reload page' );
        });
    }
}
var getExistPos = function() { 
    if (!isLoad){
        $.get( '/position/getExists' ).success( function(pos_info) {
            var pos_num = 1;
            $.each(pos_info, function() {
                $( '#add_new_pos' ).click();
                $( '#pos_name'+pos_num).val(this.name);
                $( '#sphere_'+pos_num)[0].selectedIndex = this.id_inds - 1;
                $( '#schedule_'+pos_num)[0].selectedIndex = this.id_schd - 1;        
                $( '#scheduleTrip_'+pos_num)[0].selectedIndex = this.id_trip - 1;                 
                $( '#min_wage_input_'+pos_num).val(this.min_wage);
                $( '#max_wage_input_'+pos_num).val(this.max_wage);  
                $( '#pos_info'+pos_num).val(this.info);                 
                $( '#exp_'+pos_num).val(this.experience);              
                var k = 1;             
                $.each( this.lang, function() {
                    $('#add_lang'+pos_num).click(); 
                    $('#lang_'+pos_num+"_"+k)[0].selectedIndex = this.id_lang - 1;
                    $('#llev_'+pos_num+"_"+k)[0].selectedIndex = this.id_llev - 1;                
                    k++;
                });  
                var k = 1; 
                $.each( this.educ, function() {
                    $('#add_educ'+pos_num).click(); 
                    $('#univ_'+pos_num+"_"+k)[0].selectedIndex = this.id_univ - 1;
                    $('#spec_'+pos_num+"_"+k).val(this.specialty);                
                    k++;
                }); 

                pos_num += 1;
            });  
            isLoad = true;               
        }).error( function() {
            alert( 'Error: try reload page' );
        });
    }else{
        alert('reload page to refresh information')
    }
} 

var getEduInfo = function() {
    $.get( '/fill/info' ).success( function(full_info) {
        $.each( full_info.univ, function() {
            univ.push(this);     
        });

        $.each( full_info.lang, function() {
            lang.push(this);     
        });
        $.each( full_info.llev, function() {
            llev.push(this);     
        });   
        $.each( full_info.trip, function() {
            trip.push(this);     
        });
        $.each( full_info.sphere, function() {
            sphere.push(this);     
        });     
        $.each( full_info.schedule, function() {
            schedule.push(this);     
        }); 
        getExistPos();
    }).error( function() {
        alert( 'Error: try reload page' );
    });
};

var SavePos = function(num,lang_pos,educ_pos) {
    var sendable = true;
    var univ_ids = [];
    var specialities = [];
    var lang_ids = [];
    var llev_ids = [];

    for (var k = 1; k < lang_pos; k++){
        if ($('#lang_'+num+"_"+k)[0] != null){        
            var lang_id = $('#lang_'+num+"_"+k)[0].selectedIndex+1;
            if (jQuery.inArray(lang_id, lang_ids) > -1){
                alert("Уберите дублирование названия языка: "+ $('#lang_'+num+"_"+k)[0].options[lang_id-1].text);
                sendable = false;
            }else{
                lang_ids.push(lang_id);
                llev_ids.push($('#llev_'+num+"_"+k)[0].selectedIndex+1);
            }
        }
    }


    for (var k = 1; k < educ_pos; k++){
        if ($('#univ_'+num+"_"+k)[0] != null){
            var univ_id = $('#univ_'+num+"_"+k)[0].selectedIndex+1;
            var spec_val = $('#spec_'+num+"_"+k).val();
            // alert($('#univ_'+num+"_"+k)[0].selectedIndex+1);
        // if ((univ_id != null) && (spec_val != null)){
            if ((jQuery.inArray(univ_id, univ_ids) > -1)&&(jQuery.inArray(spec_val, specialities) == jQuery.inArray(univ_id, univ_ids))) {
                alert("Уберите дублирование университета и специальности: "+ $('#univ_'+num+"_"+k)[0].options[univ_id-1].text + "\nСпециальность: " + spec_val);
                sendable = false;
            }else{             
                univ_ids.push(univ_id);
                specialities.push(spec_val);
            }
        }
    }
    // alert(sendable);
    if(sendable){
        var send_list = {};          
        send_list['pos_id'] = num;
        send_list['pos_name'] = ($('#pos_name'+num).val());
        send_list['pos_info'] = ($('#pos_info'+num).val());
        send_list['id_sphere'] = ($('#sphere_'+num)[0].selectedIndex+1);    
        send_list['id_schedule'] = ($('#schedule_'+num)[0].selectedIndex+1);       
        send_list['id_trip'] = ($('#scheduleTrip_'+num)[0].selectedIndex+1);  
        if ($('#min_wage_input_'+num).val().length > 0 ) 
            send_list['min_wage'] = ($('#min_wage_input_'+num).val());    
        if  ($('#max_wage_input_'+num).val().length > 0)     
            send_list['max_wage'] = ($('#max_wage_input_'+num).val()); 
        send_list['info'] = ($('#pos_info'+num).val());
        if  ($('#exp_'+num).val().length > 0)      
            send_list['exp'] = ($('#exp_'+num).val());

        send_list['lang_ids'] = lang_ids; 
        send_list['llev_ids'] = llev_ids;     
        send_list['univ_ids'] = univ_ids; 
        send_list['specialities'] = specialities; 
        send_list['num_lang'] = lang_ids.length;  
        send_list['num_edu'] = univ_ids.length; 
        $.post('/position/save', $.param(send_list, true), 'json').success( function() {
            alert('Successfully saved')
        }).error( function() {
            alert( 'Error: try reload page' );
        });
    }
};


var Status2Text = function(num){
    switch (num) {
        case 0:
            return "Соискатель более не заинтересован в вакансии"           
        case -1:
            return "Претендент откликнулся на вакансию"
        case -2:
            return "Вы предложили пройти собеседование"
        case -3:
            return "Претендент согласился пройти собеседование"
        case -4:
            return "Вы готовы сделать предложение о работе"
        case -5:
            return "Претендент подтвердил свою готовность приступить к работе"
        default:
        alert('Я таких значений не знаю')
    }
}

var getResumeInfo = function(){
    // alert("test")
    $.get( '/position/resume' ).success( function(posres) {
        $("div.inputs_resm").empty();
        $.each( posres, function() {
            var buttonstext = ''
            if(this.status == 0){
                buttonstext = '<input id = "denied_posres'+this.id+'" type = "button" style="width:35%;" value = "Удалить из списка" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'
            }else if(this.status == -5){
                buttonstext = '<input id = "denied_posres'+this.id+'" type = "button" style="width:35%;" value = "Удалить из списка" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'
            }else{
                buttonstext = '<input id = "denied_posres'+this.id+'" type = "button" style="width:35%;" value = "Отказать" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'+
              '<input id = "accept_posres'+this.id+'" type = "button" style="width:35%;" value = "Принять" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>';
            }
            $('<div id="posres_field'+this.id+'">'+
            '<div class="title" id="title_'+this.id+'" style="font-size:14px; color:#4527d7">Вакансия: '+this.position+
            '<br />Имя соискателя: '+this.name+
            '<br />Статус: <label  id="posres_status'+this.id+'">'+Status2Text(this.status)+'</label ></div>'+
            '<div class="inner" style = "display: none;font-size:12px;">' +  
            // '<label for = "posres_status"><b>Состояние:</b> '+'</label>'+'<label  id="posres_status'+this.id+'">'+Status2Text(this.status)+'</label >'+                
            // '<label for = "posres_name"> Имя соискателя: '+this.name+'</label>'+  
            '<label for = "posres_skills"> Навыки соискателя: '+this.skills+'</label>'+ 
            '<label for = "posres_post"> Желаемая должность: '+this.post+'</label>'+    
            '<label for = "posres_wage"> Желаемая з/п: '+this.wage+'</label>'+    
            '<label for = "posres_exp"> Опыт работы в данной сфере: '+this.exp+' г.</label>'+                
            '<label for = "posres_schd"> График работы: '+this.schd+'</label>'+    
            '<label for = "posres_trip"> График командировок: '+this.trip+'</label>'+  
            '<label for = "posres_lan"> Владение языками: '+this.lan+'</label>'+ 
            '<label for = "posres_educ"> Образование: '+this.educ+'</label>'+     
            '<label for = "posres_email"> Email для связи с соискателем: '+this.email+'</label>'+                  
            '<hr />'+
            buttonstext+
            '<hr />'+                 
            '</div>'+
            '</div>').fadeIn('slow').appendTo('.inputs_resm');
            
            $('#title_'+this.id).click(function(){
                $(this).next('.inner').stop().slideToggle();
            }); 
            $('#denied_posres'+this.id).click(function() {
                if (confirm("Вы подтверждаете удаление? После подтверждения данное резюме больше не будет показываться в списке.")) {
                    var cur_id = this.id.substring(13);
                    if (($(this).attr("value") == "Отказать")){    
                        $.get( '/position/denied?id=' + cur_id).success( function() {
                            alert("отказ подтвержден");
                            $('#posres_field'+cur_id).remove();
                        });
                    }else{
                        $.get( '/position/deleted?id=' + cur_id).success( function() {
                            alert("резюме удалено из списка");
                            $('#posres_field'+cur_id).remove();   
                        });                            
                    }                           
                }
            });  

 
            $('#accept_posres'+this.id).click(function() {
                var cur_id = this.id.substring(13);
                $.get( '/position/accept?id=' + cur_id).success( function(status) { 
                    alert("подтверждение отправлено ");
                    $('#posres_status'+cur_id).text(Status2Text(status));
                    if (status == 0){
                        $( '#show_resm' ).click();                        
                        $( '#show_resm' ).click();
                    }
              });
            });                  
        });

    });
}


$( function() {
    // Setup UI
    $( 'input:button' ).button();
    $( '#fdate' ).datepicker({ 
        defaultDate: "0",
        dateFormat: "dd.mm.yy", 
        changeYear: true 
    });
    $('#fdate').datepicker( "setDate", "0");  

    var isInfoClick = false;   
    var isPosClick = false; 
    var isResmClick = false;
    $( '#input_info' ).click( function() {
        if( !isInfoClick ){
            getAbout();
            $( '#add_info' ).hide().fadeIn();   
            $( '#add_pos' ).hide(); 
            $( '#resumes' ).hide();                       
        }            
        else
            $( '#add_info' ).hide();   
        
        isInfoClick = !isInfoClick;
        isPosClick = false;
    });   

    $( '#create_pos' ).click( function() {
        if( !isPosClick ){
            getEduInfo();
            $( '#add_pos' ).hide().fadeIn();   
            $( '#add_info' ).hide(); 
            $( '#resumes' ).hide();                       
        }            
        else{
            $( '#add_pos' ).hide();      
            univ = new Array();
            lang = new Array();
            llev = new Array();
            trip = new Array();
            sphere = new Array();
            schedule = new Array(); 
        }
        isPosClick = !isPosClick;
        isInfoClick = false;
    });   
    
    $( '#show_resm' ).click( function() {
        if( !isResmClick ){
            getResumeInfo();
            $( '#resumes' ).hide().fadeIn();             
            $( '#add_pos' ).hide();   
            $( '#add_info' ).hide();           
        }            
        else{
            $( '#resumes' ).hide(); 
        }
        isResmClick = !isResmClick;
        isPosClick = false;
        isInfoClick = false;
    });       

    var checkNum = function(num){
        $(num).keydown(function(event) {
            // Разрешаем нажатие клавиш backspace, del, tab и esc
            if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || 
                 // Разрешаем выделение: Ctrl+A
                (event.keyCode == 65 && event.ctrlKey === true) || 
                 // Разрешаем клавиши навигации: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                     return;
            }
            else {
                // Запрещаем всё, кроме клавиш цифр на основной клавиатуре, а также Num-клавиатуре
                if ((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault(); 
                }   
            }
        });
    };
    var checkFloatNum = function(num){
        $(num).keyup(function(event) {
            // Разрешаем нажатие клавиш точки backspace, del, tab и esc
            if ( event.keyCode == 46 || event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || 
                 // Разрешаем выделение: Ctrl+A
                (event.keyCode == 65 && event.ctrlKey === true) || 
                 // Разрешаем клавиши навигации: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                     return;
            }
            else {
                    if(!(/^\d+\.\d+$/.test($(num).val()))&&!(/^\d+$/.test($(num).val()))&&!(/^\d+\.$/.test($(num).val()))){
                        $(num).val($(num).val().slice(0, -1));
                    }
                  }
        });
    };

    $('#save_info').click( function() {
        var send_list = {};
        send_list['date'] = String($('#fdate').val());      
        send_list['about'] = $('#info').val();  
        $.post('/position/save_about', $.param(send_list, true), 'json').success( function() {
        }).error( function() {
            alert( 'Error: try reload page' );
        });
    }); 

    var pos_num = 1
    $( '#add_new_pos' ).click( function() {
        var trip_select ='';
        var schedule_select ='';
        var sphere_select = '';
        for (var k = 0; k < window.trip.length; k++){
            trip_select = trip_select + '<option value="'+k+'">"'+window.trip[k]+'"</option>';
        }        
        for (var k = 0; k < window.schedule.length; k++){
            schedule_select = schedule_select + '<option value="'+k+'">"'+window.schedule[k]+'"</option>';
        }    
        for (var k = 0; k < window.sphere.length; k++){
            sphere_select = sphere_select + '<option value="'+k+'">"'+window.sphere[k]+'"</option>';
        }  
        $('<div id="pos_field'+pos_num+'"><label for = "pos">Позиция</label>'+
            '<label for = "pos_name">Название позиции</label>'+
            '<input type = "text" id = "pos_name'+pos_num+
            '" class = "ui-widget-content ui-corner-all"  style="width:70%;"/>'+   
            '<label for = "pos_info">О позиции</label>'+
            '<textarea rows="4" cols="40" class = "ui-widget-content ui-corner-all" id="pos_info'+pos_num+'"  style="width:70%;"></textarea>' +          
            '<label for = "sphere">Отрасль(обязательное поле)</label>'+
            '<select id="sphere_' + pos_num + '" style="width:70%;">'+ sphere_select + '</select>'+
            '<label for = "schedule">График работы(обязательное поле)</label>'+
            '<select id="schedule_' + pos_num + '" style="width:70%;">'+ schedule_select + '</select>'+ 
            '<label for = "scheduleTrip">График командировок(обязательное поле)</label>'+
            '<select id="scheduleTrip_' + pos_num + '" style="width:70%;">'+ trip_select + '</select>'+  
            '<label for = "min_wage_input">Минимальная заработная плата</label>'+
            '<input type = "text" id = "min_wage_input_'+pos_num+
            '" class = "ui-widget-content ui-corner-all"/>'+  
            '<label for = "max_wage_input">Максимальная заработная плата</label>'+
            '<input type = "text" id = "max_wage_input_'+pos_num+
            '" class = "ui-widget-content ui-corner-all" />'+        
            '<label for = "exp">Опыт работы в аналогичной сфере</label>'+
            '<input type = "text" id = "exp_'+pos_num+
            '" class = "ui-widget-content ui-corner-all" />'+     
            '<hr /><div class="inputs_lang' + pos_num + '">'+
            '<input id = "add_lang'+pos_num+'" type = "button" style="width:35%;" value = "Добавить языковые требования к кандидату" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false" />'+    
            '</div>'+
            '<hr /><div class="inputs_educ' + pos_num + '">'+
            '<input id = "add_educ'+pos_num+'" type = "button" style="width:35%;" value = "Добавить ожидаемое от кандидата образование" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'+ 
            '</div>'+  
            '<hr /><input id = "rm_pos'+pos_num+'" type = "button" style="width:35%;" value = "Удалить позицию" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'+
            '<input id = "sv_pos'+pos_num+'" type = "button" style="width:35%;" value = "Сохранить позицию" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'+
            '<hr /><hr color="white" size="20" /><hr /></div>').fadeIn('slow').appendTo('.inputs_pos');

        $('#rm_pos'+pos_num).click(function() {
            if (confirm("Вы подтверждаете закрытие вакансии? После подтверждения данная вакансия больше не будет показываться в списке.")) {
                var cur_id = this.id.substring(6);
                $.get( '/position/close?id=' + cur_id).success( function() {
                    alert("Вакансия закрыта");
                    $('#pos_field'+cur_id).remove(); 
                });                
            }       
        }); 

        var lang_pos = 1;
        $('#add_lang'+pos_num).click(function() {
            var n = this.id.substring(8)
            var lang_select ='';
            var llev_select ='';
            for (var k = 0; k < window.lang.length; k++){
                lang_select = lang_select + '<option value="'+k+'">"'+window.lang[k]+'"</option>';
            }        
            for (var k = 0; k < window.llev.length; k++){
                llev_select = llev_select + '<option value="'+k+'">"'+window.llev[k]+'"</option>';
            }             
            $('<div id="lang_field' + n + "_"+ lang_pos + '" class = "ui-state-active" style="width:80%;"><label for = "lang">Язык</label>'+
            '<select id="lang_' + n + "_"+ lang_pos + '" style="width:70%;">'+ lang_select + '</select>'+
            '<label for = "llev">Уровень владения языком</label>'+
            '<select id="llev_' + n + "_"+ lang_pos + '" style="width:70%;">'+ llev_select + '</select>'+
            '<input id = "rm_lang' + n + "_"+lang_pos+'" type = "button" style="width:35%;" value = "Удалить язык" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'+
            '</div>').fadeIn('slow').appendTo('.inputs_lang'+n);
            $('#rm_lang'+ + n + "_"+lang_pos).click(function() {
                $('#lang_field'+this.id.substring(7)).remove();
            }); 
            lang_pos++;    
        }); 
        var educ_pos = 1;
        $('#add_educ'+pos_num).click(function() {
            var n = this.id.substring(8)
            var univ_select ='';
            for (var k = 0; k < window.univ.length; k++){
                univ_select = univ_select + '<option value="'+k+'">"'+window.univ[k]+'"</option>';
            }        
           
            $('<div id="educ_field' + n + "_"+ educ_pos + '" class = "ui-state-active" style="width:80%;"><label for = "univ">Университет</label>'+
            '<select id="univ_' + n + "_"+ educ_pos + '" style="width:70%;">'+ univ_select + '</select>'+
            '<label for = "spec">Специальность</label>'+
            '<input type = "text" id = "spec_' + n + "_"+educ_pos+
            '" class = "ui-widget-content ui-corner-all" style="width:70%;" />'+
            '<input id = "rm_educ' + n + "_"+educ_pos+'" type = "button" style="width:35%;" value = "Удалить образование" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'+
            '</div>').fadeIn('slow').appendTo('.inputs_educ'+n);
            $('#rm_educ' + n + "_"+educ_pos).click(function() {
                $('#educ_field'+this.id.substring(7)).remove();
            }); 
            educ_pos++;   
        });         

        $('#sv_pos'+pos_num).click(function() {
            SavePos(this.id.substring(6),lang_pos,educ_pos);

        });       

        checkNum("#min_wage_input_"+pos_num);
        checkNum("#max_wage_input_"+pos_num);
        checkFloatNum("#exp_"+pos_num);

        pos_num ++;
        
    });        
});