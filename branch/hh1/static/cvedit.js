'use strict';

var univ = new Array();
var tedu = new Array();
var lang = new Array();
var llev = new Array();
var trip = new Array();
var sphere = new Array();
var schedule = new Array();


var register = function( nm, snm, tnm, btd, e_mail, password ) {

    var query = '/user/register?nm='+nm+'&snm=' + snm+'&tnm=' + tnm+'&btd=' + btd+'&e_mail=' + e_mail+'&password=' + password;

    $.get( query ).success( function(par) {
        if (par == 'register success'){
            window.location.reload();
        }
        else{
            alert( par );
        }
        
    }).error( function() {
        alert( 'This e-mai already exists' );
    });

};

var logIn = function( e_mail, password ) {

    var query = '/user/login?e_mail=' + e_mail+'&password=' + password;
    $.get( query ).success( function() {
        window.location.reload();              
    }).error( function() {
        alert( 'Invalid e-mail or password' );
    });

};

var logOut = function() {
    $.get( '/user/logout', function() {
        window.location.reload();
    });
};

var getEduInfo = function() {
    $.get( '/education/info' ).success( function(educ_full_info) {
        $.each( educ_full_info.univ, function() {
            univ.push(this);     
        });
        $.each( educ_full_info.tedu, function() {
            tedu.push(this);     
        });     
        $.each( educ_full_info.lang, function() {
            lang.push(this);     
        });
        $.each( educ_full_info.llev, function() {
            llev.push(this);     
        });   
    });
};

var getCVInfo = function() { 
    $.get( '/cv/info' ).success( function(cv_full_info) {
        $.each( cv_full_info.trip, function() {
            trip.push(this);     
        });
        $.each( cv_full_info.sphere, function() {
            sphere.push(this);     
        });     
        $.each( cv_full_info.schedule, function() {
            schedule.push(this);     
        });
    });
}; 

var Status2Text = function(num){
    if (num > 0)
        return "Ожидание подтверждения готовности рассмотреть вакансию"
    else{
        switch (num) {
            case 0:
                return "Вам ответили отказом"                        
            case -1:
                return "Вы откликнулись"
            case -2:
                return "Вам предложили пройти собеседование"
            case -3:
                return "Вы согласились пройти собеседование"
            case -4:
                return "Вам готовы сделать предложение о работе"
            case -5:
                return "Вы подтвердили свою готовность приступить к работе"
            case -6:
                return "Данная вакансия закрыта"        
            default:
            alert('Я таких значений не знаю')
        }

    }

}

var getPositionsInfo = function(){
    $.get( '/positions/info' ).success( function(positions) {
        $("div.inputs_pos").empty();
        $.each( positions, function() {
            var buttonstext = ''
            if(this.status == 0){
                buttonstext = '<input id = "denied_pos'+this.id+'" type = "button" style="width:35%;" value = "Удалить из списка" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'
            }else if(this.status <= -5){
                buttonstext = '<input id = "denied_pos'+this.id+'" type = "button" style="width:35%;" value = "Удалить из списка" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'
            }else{
                buttonstext = '<input id = "denied_pos'+this.id+'" type = "button" style="width:35%;" value = "Отказать" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>'+
              '<input id = "accept_pos'+this.id+'" type = "button" style="width:35%;" value = "Принять" class="ui-button ui-widget ui-state-default ui-corner-all ui-state-hover" aria-disabled="false"/>';
            }
            $('<div id="pos_field'+this.id+'">'+
              '<label for = "pos_status"><b>Состояние:</b> '+'</label>'+'<label  id="pos_status'+this.id+'">'+Status2Text(this.status)+'</label >'+                
              '<label for = "pos_name"><b>Название вакансии:</b> '+this.name+'</label>'+
              '<label for = "pos_info"> <p /><b>Информация о вакансии:</b> '+this.info+'</label>'+
              '<label for = "pos_schd"> <p /><b>График работы:</b> '+this.schd+'</label>'+              
              '<label for = "pos_trip"> <p /><b>Командировки:</b> '+this.trip+'</label>'+   
              '<label for = "pos_trip"> <p /><b>Зарплата:</b> </label>'+                 
              '<label for = "pos_min_wage"> От: '+this.min_wage+'</label>'+   
              '<label for = "pos_max_wage"> До: '+this.max_wage+'</label>'+        
              '<label for = "pos_experience"> <p /><b>Опыт работы:</b> '+this.experience+'</label>'+     
              '<label for = "pos_lan"> <p /><b>Знание языков:</b>  <br />'+this.lan.replace(';', ';<br />  ')+'</label>'+               
              '<label for = "pos_educ"> <p /><b>Предпочитаются выпускники:</b> <br />'+this.educ.replace(';', ';<br />  ')+'</label>'+
              '<hr />'+
              buttonstext+
              '<hr /><hr color="white" size="20" /><hr /></div>').fadeIn('slow').appendTo('.inputs_pos');    
            
            $('#denied_pos'+this.id).click(function() {
                if (confirm("Вы подтверждаете удаление? После подтверждения данная вакансия больше не будет показываться в списке.")) {
                    var cur_id = this.id.substring(10);
                    if (($(this).attr("value") == "Отказать")){
                        $.get( '/positions/denied?id=' + cur_id).success( function() {
                            alert("отказ подтвержден");
                            $('#pos_field'+cur_id).remove();
                        });                
                    }else{
                        $.get( '/positions/deleted?id=' + cur_id).success( function() {
                            alert("вакансия удалена из списка");
                            $('#pos_field'+cur_id).remove();       
                        });                    
                    }    
                }
            });  
            if (this.status != 0){
                $('#accept_pos'+this.id).click(function() {
                    var cur_id = this.id.substring(10);
                    // $('#pos_status'+cur_id).text('тест');
                    // alert('#pos_status'+cur_id)
                    $.get( '/positions/accept?id=' + cur_id).success( function(status) { 
                        alert("отклик отправлен ");
                        $('#pos_status'+cur_id).text(Status2Text(status));
                        if (status == 0 || status <= -5){
                            $( '#show_pos' ).click();                            
                            $( '#show_pos' ).click();
                        }
                     // изменить строку состояния
                    // сделать отправку статуса confirm на оо и отметить в своей базе статус -1, -3, -5 (в соотв с текущим)
                  });
                });    
            }              
        });
    });
}


$( function() {
    // Setup UI
    $( 'input:button' ).button();
    $( '#birthday_input' ).datepicker({ 
        minDate:  "-150y",
        maxDate: "-18y",
        defaultDate: "0",
        dateFormat: "dd.mm.yy", 
        changeYear: true 
    });
    $('#birthday_input').datepicker( "setDate", "-18y");    

    $( '#register_form' ).dialog({
        autoOpen: false,
        modal: true
    });
    $( '#login_form' ).dialog({
        autoOpen: false,
        modal: true
    });

//-------------------------------------------------

var next_univ_num = $('univ_field').size() + 1;    
    $('#add_univ').click(function() {
        var univ_select = '';
        var tedu_select = '';

        for (var k = 0; k < window.univ.length; k++){
            univ_select = univ_select + '<option value="'+k+'">"'+window.univ[k]+'"</option>';
        }        
        for (var k = 0; k < window.tedu.length; k++){
            tedu_select = tedu_select + '<option value="'+k+'">"'+window.tedu[k]+'"</option>';
        }
 
        $('<div class="univ_field"><label for = "univ">Введите название ВУЗа</label>'+
        '<select id="univ_' + next_univ_num +'">'+ univ_select+ '</select>'+
        '<label for = "tedu">Введите тип обучения</label>'+
        '<select id="tedu_' + next_univ_num +'">'+ tedu_select+ '</select>'+
        '<label for = "spec">Специальность</label>'+
        '<input type = "text" id = "spec_' + next_univ_num + '" class = "ui-widget-content ui-corner-all"></input>'+
        '<label for = "grad_day_input">Дата окончания обучения</label>'+
        '<input type = "text" readonly="true" id = "grad_day_input_'+next_univ_num+
        '" class = "ui-widget-content ui-corner-all" /><hr /></div>').fadeIn('slow').appendTo('.inputs_univ');
        $( '#grad_day_input_'+next_univ_num ).datepicker({ 
            minDate:  "-150y",
            dateFormat: "dd.mm.yy", 
            defaultDate: "0",
            changeYear: true       
        }); 

       $('#grad_day_input_'+next_univ_num).datepicker( "setDate", "0");

        next_univ_num++;
        if(next_univ_num == 2){
            $( '#rm_u_button' ).hide().fadeIn();
        }
    });

    var next_lang_num = $('lang_field').size() + 1;
    $('#add_lang').click(function() {
        var lang_select ='';
        var llev_select ='';
        for (var k = 0; k < window.lang.length; k++){
            lang_select = lang_select + '<option value="'+k+'">"'+window.lang[k]+'"</option>';
        }        
        for (var k = 0; k < window.llev.length; k++){
            llev_select = llev_select + '<option value="'+k+'">"'+window.llev[k]+'"</option>';
        } 
        
        $('<div class="lang_field"><label for = "lang">Язык</label>'+
        '<select id="lang_' + next_lang_num + '">'+ lang_select + '</select>'+
        '<label for = "llev">Уровень владения языком</label>'+
        '<select id="llev_' + next_lang_num + '">'+ llev_select + '</select>'+'<hr /></div>').fadeIn('slow').appendTo('.inputs_lang');
        next_lang_num++;
        if(next_lang_num == 2){
            $( '#rm_l_button' ).hide().fadeIn();
        }
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

    var next_resume_num = $('resume_field').size() + 1;
    $('#add_new_resume').click(function() {
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
        
        $('<div class="resume_field">'+
            '<div class="title" id="title_'+next_resume_num+'" style="font-size:19px; color:#4297d7">Резюме '+next_resume_num+'</div>'+
            '<div class="inner">'+
            '<label for = "sphere">Отрасль(обязательное поле)</label>'+
            '<select id="sphere_' + next_resume_num + '">'+ sphere_select + '</select>'+
            '<label for = "schedule">График работы(обязательное поле)</label>'+
            '<select id="schedule_' + next_resume_num + '">'+ schedule_select + '</select>'+ 
            '<label for = "scheduleTrip">График командировок(обязательное поле)</label>'+
            '<select id="scheduleTrip_' + next_resume_num + '">'+ trip_select + '</select>'+  
            '<label for = "min_wage_input">Минимальная заработная плата</label>'+
            '<input type = "text" id = "min_wage_input_'+next_resume_num+
            '" class = "ui-widget-content ui-corner-all" />'+  
            '<label for = "max_wage_input">Максимальная заработная плата</label>'+
            '<input type = "text" id = "max_wage_input_'+next_resume_num+
            '" class = "ui-widget-content ui-corner-all" />'+        
            '<label for = "post">Желаемая должность</label>'+
            '<input type = "text" id = "post_'+next_resume_num+
            '" class = "ui-widget-content ui-corner-all" />'+    
            '<label for = "post">Опыт работы в аналогичной сфере(обязательное поле)</label>'+
            '<input type = "text" id = "exp_'+next_resume_num+
            '" class = "ui-widget-content ui-corner-all" />'+                
            '<label for = "skills">Опишите свои навыки</label>'+
            '<textarea rows="4" cols="40" class = "ui-widget-content ui-corner-all" id="skills_'+next_resume_num+'"></textarea>' +          
            '</div></div>').fadeIn('slow').appendTo('.inputs_resume');

        $('#title_'+next_resume_num).click(function(){
            $(this).next('.inner').stop().slideToggle();
        });

        checkNum("#min_wage_input_"+next_resume_num);
        checkNum("#max_wage_input_"+next_resume_num);
        checkFloatNum("#exp_"+next_resume_num);

        next_resume_num++;
        if(next_resume_num == 2){
            $( '#rm_r_button' ).hide().fadeIn();
        }/**/
    });
   

    $('#remove_univ').click(function() {
        if(next_univ_num > 1) {
            $('.univ_field:last').remove();
            next_univ_num--;
        }
        if(next_univ_num == 1){
            $( '#rm_u_button' ).hide();
        }
    });

    $('#remove_lang').click(function() {
        if(next_lang_num > 1) {
            $('.lang_field:last').remove();
            next_lang_num--;
        }
        if(next_lang_num == 1){
            $( '#rm_l_button' ).hide();
        }
    });   

    $('#remove_resume').click(function() {
        if(next_resume_num > 1) {
            $('.resume_field:last').remove();
            next_resume_num--;
        }
        if(next_resume_num == 1){
            $( '#rm_r_button' ).hide();
        }
    }); 

var resetUniv = function() {
        while(next_univ_num > 1) {
            $('.univ_field:last').remove();
            next_univ_num--;
        }
        $( '#rm_u_button' ).hide();
    };

var resetLang = function() {
        while(next_lang_num > 1) {
            $('.lang_field:last').remove();
            next_lang_num--;
        }
        $( '#rm_l_button' ).hide();
    };
var resetResume = function() {
        while(next_resume_num > 1) {
            $('.resume_field:last').remove();
            next_resume_num--;
        }
        $( '#rm_r_button' ).hide();
    };    
//-------------------------------------------------    
    $( '#save_ei' ).click( function() {//save_ei
        var univ_ids = [];
        var specialities = [];
        var year_grads = [];
        var tedu_ids = [];
        var lang_ids = [];
        var llev_ids = [];
        var send_list = {};
        var sendable = true;
        send_list['num_edu'] = next_univ_num-1;
        send_list['num_lang'] = next_lang_num-1;
        for (var k = 1; k < next_univ_num; k++){
            var univ_id = $('#univ_'+k)[0].selectedIndex+1;
            var spec_val = $('#spec_'+k).val();
            if ((jQuery.inArray(univ_id, univ_ids) > -1)&&(jQuery.inArray(spec_val, specialities) == jQuery.inArray(univ_id, univ_ids))) {
                alert("Уберите дублирование университета и специальности: "+ $('#univ_'+k)[0].options[univ_id-1].text + "\nСпециальность: " + spec_val);
                sendable = false;
            }else{             
                univ_ids.push(univ_id);
                specialities.push(spec_val);
                year_grads.push($('#grad_day_input_'+k).val());
                tedu_ids.push($('#tedu_'+k)[0].selectedIndex+1);      
            }
        }
        if(next_univ_num > 1){
            send_list['univ_ids'] = univ_ids;
            send_list['specialities'] = specialities;            
            send_list['year_grads'] = year_grads;
            send_list['tedu_ids'] = tedu_ids;            
        }
        for (var k = 1; k < next_lang_num; k++){
            var lang_id = $('#lang_'+k)[0].selectedIndex+1;
            if (jQuery.inArray(lang_id, lang_ids) > -1){
                alert("Уберите дублирование названия языка: "+ $('#lang_'+k)[0].options[lang_id-1].text);
                sendable = false;
            }else{
               lang_ids.push(lang_id); 
               llev_ids.push($('#llev_'+k)[0].selectedIndex+1);
            }               
        }  
        if(next_lang_num > 1){
            send_list['lang_ids'] = lang_ids;
            send_list['llev_ids'] = llev_ids;            
        }
        
        if(sendable)
            $.post('/usereduc/save_ei', $.param(send_list, true), 'json').success( function() {
                    alert("Изменения сохранены")
                }).error( function() {
                    alert( 'Error: try reload page' );
                });
    });     

    $( '#save_cv' ).click( function() {//save_ei
        var id_sphere = [];
        var id_schedule = [];
        // var schedule = [];
        var id_trip = [];
        // var trip = [];
        var post = [];
        var min_wage = [];
        var max_wage = [];
        var skills = [];
        var exp = [];
        var send_list = {};
        var sendable = true;

        send_list['num_resume'] = next_resume_num-1;
        for (var k = 1; k < next_resume_num; k++){
            var id_sph = $('#sphere_'+k)[0].selectedIndex+1;            
            var p = $('#post_'+k).val();
            if (jQuery.inArray(id_sph, id_sphere) > -1) {
                alert("Уберите дублирование резюме с одинаковой отраслью : "+ 
                    $('#sphere_'+k)[0].options[id_sph-1].text);
                sendable = false;
            }else{      
                id_sphere.push(id_sph);
                post.push(p);
                id_trip.push($('#scheduleTrip_'+k)[0].selectedIndex+1);
                id_schedule.push($('#schedule_'+k)[0].selectedIndex+1);  
                min_wage.push($('#min_wage_input_'+k).val());  
                max_wage.push($('#max_wage_input_'+k).val());    
                skills.push($('#skills_'+k).val());         
                exp.push($('#exp_'+k).val());      
            }
        }

        if(next_resume_num > 1){
            send_list['id_sphere'] = id_sphere;
            send_list['id_schedule'] = id_schedule;            
            send_list['id_trip'] = id_trip;
            send_list['post'] = post;  
            send_list['min_wage'] = min_wage;
            send_list['max_wage'] = max_wage;            
            send_list['skills'] = skills;
            send_list['exp'] = exp;                

        }

        if(sendable)
            $.post('/usercv/save_cv', $.param(send_list, true), 'json').success( function() {
                    alert("Изменения сохранены")
                     $.get( '/__mail_thread/info' ).success( function(info) {
                        alert(info);
                     });   
                }).error( function() {
                    alert( 'Error: try reload page' );
                });
    });     

//-------------------------------------------------
var getUserEduInfo = function() { 
    $.get( '/usereduc/eduInfo' ).success( function(user_educ_info) {
        // window.location.reload();
        if(user_educ_info.num_edu > 0){
            if(user_educ_info.num_edu > 1){
                var k = 1;
                $.each( user_educ_info.year_grad, function() {
                    $('#add_univ').click(); 
                    $('#grad_day_input_'+k).datepicker('setDate', this);
                    k++;
                });    
                k = 1;
                $.each( user_educ_info.id_univ, function() {
                    $('#univ_'+k)[0].selectedIndex = this;
                    k++;
                }); 
                k = 1;
                $.each( user_educ_info.id_tedu, function() {
                    $('#tedu_'+k)[0].selectedIndex = this;  
                    k++;
                }); 
                k = 1;
                $.each( user_educ_info.specialty, function() {
                    $('#spec_'+k).val(this);                      
                    k++;
                }); 

            }
            else{                
                $('#add_univ').click(); 
                $('#grad_day_input_1').datepicker('setDate', String(user_educ_info.year_grad));
                $('#univ_1')[0].selectedIndex = user_educ_info.id_univ;
                $('#tedu_1')[0].selectedIndex = user_educ_info.id_tedu;  
                $('#spec_1').val(user_educ_info.specialty);  
            }
        };
        if(user_educ_info.num_lang > 0){
            if(user_educ_info.num_lang > 1){
                k = 1;
                $.each( user_educ_info.id_lang, function() {
                    $('#add_lang').click(); 
                    $('#lang_'+k)[0].selectedIndex = this;
                    k++;
                });    
                k = 1;
                $.each( user_educ_info.id_llev, function() {
                    $('#llev_'+k)[0].selectedIndex = this;
                    k++;
                }); 
            }
            else{                
                $('#add_lang').click(); 
                $('#lang_1')[0].selectedIndex = user_educ_info.id_lang;
                $('#llev_1')[0].selectedIndex = user_educ_info.id_llev;  
            }  
        }
    });
}; 

var getUserCVInfo = function() { 
    $.get( '/usercv/info' ).success( function(user_cv_info) {
        if(user_cv_info.num_resume > 0){
            if(user_cv_info.num_resume > 1){
                var k = 1;
                $.each( user_cv_info.id_sphere, function() {
                    $('#add_new_resume').click(); 
                    $('#sphere_'+k)[0].selectedIndex = this;
                    k++;
                });    
                k = 1;
                $.each( user_cv_info.id_schedule, function() {
                    $('#schedule_'+k)[0].selectedIndex = this;
                    k++;
                }); 
                k = 1;
                $.each( user_cv_info.id_trip, function() {
                    $('#scheduleTrip_'+k)[0].selectedIndex = this;  
                    k++;
                }); 
                k = 1;
                $.each( user_cv_info.post, function() {
                    $('#post_'+k).val(this);                      
                    k++;
                }); 
                k = 1;
                $.each( user_cv_info.min_wage, function() {
                    $('#min_wage_input_'+k).val(this);                      
                    k++;
                }); 
                k = 1;
                $.each( user_cv_info.max_wage, function() {
                    $('#max_wage_input_'+k).val(this);                      
                    k++;
                });  
                k = 1;
                $.each( user_cv_info.skills, function() {
                    $('#skills_'+k).val(this);                      
                    k++;
                });       
                k = 1;
                $.each( user_cv_info.exp, function() {
                    $('#exp_'+k).val(this);                      
                    k++;
                });                                             
            }
            else{         
                // user_cv_info.num_resume       
                $('#add_new_resume').click(); 
                $('#sphere_1')[0].selectedIndex = user_cv_info.id_sphere;
                $('#schedule_1')[0].selectedIndex = user_cv_info.id_schedule;
                $('#scheduleTrip_1')[0].selectedIndex = user_cv_info.id_trip;
                $('#post_1').val(user_cv_info.post);
                $('#min_wage_input_1').val(user_cv_info.min_wage); 
                $('#max_wage_input_1').val(user_cv_info.max_wage);
                $('#skills_1').val(user_cv_info.skills);
                $('#exp_1').val(user_cv_info.exp);  
            }
        };
 
    });
}; 

//-------------------------------------------------
var hideEduc = function(){
    $( '#education' ).hide();        
    resetUniv();
    resetLang();
    univ = [];
    tedu = [];
    lang = [];
    llev = [];
};
var hideResume = function(){
    $( '#add_resume' ).hide();        
    resetResume();
    trip = [];
    sphere = [];
    schedule = [];    
};

var isEduClick = false;
var isAddResClick = false;
var isShowPos = false;
$( '#input_edu' ).click( function() {
    if( !isEduClick ){
        $( '#education' ).hide().fadeIn();
        hideResume();
        $( '#positions' ).hide(); 
        getEduInfo();   
        getUserEduInfo();            
    }            
    else{
        hideEduc();
    }
    isEduClick = !isEduClick;
    isAddResClick = false;
    isShowPos = false;
});

$( '#create_cv' ).click( function() {
    if( !isAddResClick ){
        hideEduc();
        $( '#add_resume' ).hide().fadeIn(); 
        $( '#positions' ).hide();     
        getCVInfo();
        getUserCVInfo();
    }else
        hideResume();       
    isAddResClick = !isAddResClick;
    isEduClick = false;
    isShowPos = false;
});

$( '#show_pos' ).click( function() {
    if( !isShowPos ){
        hideEduc();
        hideResume(); 
        getPositionsInfo();
        $( '#positions' ).hide().fadeIn();             
    }            
    else
        $( '#positions' ).hide();        
    isShowPos = !isShowPos;
    isEduClick = false;
    isAddResClick = false;
});    
    
   
//-------------------------------------------------    
    $( '#register' ).click( function() {
        $( '#register_form' ).dialog( 'option', 'title', 'Register' );
        $( '#register_form' ).dialog( 'option', 'buttons', {
            "Register": function() {
                register( $('#nm_input').val(),$('#snm_input').val(),$('#tnm_input').val(),$('#birthday_input').val(),$('#e_mail_input').val(),$('#password_input').val() );
            },
            "Cancel": function() {
                $( this ).dialog( "close" );
            }
        });
        $( '#register_form' ).dialog( 'open' );
    });

    $( '#login' ).click( function() {
        $( '#login_form' ).dialog( 'option', 'title', 'Log In' );
        $( '#login_form' ).dialog( 'option', 'buttons', {
            "Log In": function() {
                logIn( $('#login_input').val(),$('#pass_input').val() );
            },
            "Cancel": function() {
                $( this ).dialog( "close" );
            }
        });
        $( '#login_form' ).dialog( 'open' );
    });

    $( '#logout' ).click( logOut );
    
    
    var authorized = false;
    $.get( '/user/info' ).success( function(user_full_info) {
        $( '#authorized_user_panel' ).fadeIn( 'slow' );
        authorized = true;
          
        $( '#user_full_name' ).text( user_full_info.surname+' '+user_full_info.name +' '+ user_full_info.thirdname );

    }).error( function() {
        $( '#unauthorized_user_panel' ).fadeIn( 'slow' );
    });
});