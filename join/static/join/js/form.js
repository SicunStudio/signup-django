$(document).ready(function(e) {
	$("#input_page #next").click(function(){
		var name,sex,class1,depart1, depart2,change,qq,tel,email;
		sex=$("select[name='sex']").val();
		if($("input[name='adjustment']").is(':checked')){
			change='是';
		}else{change='否';}
		if(name=$("#name_input").val()){
			$("#confirm_page #name").html(name);
			$("#confirm_page #sex").html(sex);
			$("#confirm_page #change").html(change);
			if(class1=$("#class1_input").val()){
				$("#confirm_page #class1").html(class1);
				depart1=$("#dream_input1").val();  depart2=$("#dream_input2").val();
				if(depart1 && depart2){
					$("#confirm_page #depart1").html(depart1);
					$("#confirm_page #depart2").html(depart2);
					if(qq=$("#qq_input").val()){
						$("#confirm_page #qq").html(qq);
						if(tel=$("#tel_input").val()){
							$("#confirm_page #tel").html(tel);
							if(email=$("#email_input").val()){
								var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
								if(!myreg.test(email)){
									alert('请输入有效的EMAIL地址！');
									$("#email_input").focus();
								}
								else{
									$("#confirm_page #email").html(email);
									if($("#special_input").val()){
										if($("#experience_input").val()){
											if($("#self_input").val()){
													$("#input_page").css("display","none");
													$("#confirm_page").css("display","block");
											}
											else{
												alert("会评价自己才能更好的进步哦，请试着评价一下吧！");
											}
										}
										else{
											alert("没有实践经历请填写无哦！");
										}
									}
									else{
										alert("少侠一定有特长，要善于发现自己，填写一下吧！");
									}
								}
							}
							else{
								alert("EMAIL不能为空");
							}
						}
						else{
							alert("TEL不能为空");
						}
					}
					else{
						alert("QQ不能为空");
					}
				}
				else{
					alert("意向部门不能为空");
				}
			}
			else{
				alert("专业班级不能为空");
			}
		}
		else{
			alert("姓名不能为空");
		}
	});
	$("#readed").click(function(){
		$("#confirm_submit").removeAttr("disabled");
	});
});

function back1(){
	$("#input_page").css("display","block");
	$("#confirm_page").css("display","none");
}