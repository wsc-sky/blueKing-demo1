<%inherit file="/base.html"/>

<%block name="content">


  <div class="container">

    <br/>

    <div class="king-block king-block-bordered">
      <div class="king-block-header king-gray-light">
        <h3 class="king-block-title">填写个人信息</h3>
      </div>
      <div class="king-block-content">
        选择业务

        <select id="business_select" name="select_job" class="select2_box" onchange="select_job()" style="width: 200px">
          %for app in app_list:
            <option value=${str(app['ApplicationID'])+'~'+app['ApplicationName']} class="selected_job"
                    selected=${app['ApplicationID']=="3"}>${app['ApplicationName']}
            </option>
          %endfor
        </select>

        任务类型

        <select name="select_task" id="select_task" class="select2_box" style="width: 200px">
          <option value="" class="selected_task" selected="true">
          %for task in task_list:
            <option id="" value=${str(task['id'])+'~'+task['name']} class="selected_task">${task['name']}</option>
          %endfor

        </select>
      </div>
    </div>
    <div class="king-block king-block-bordered">
      <div class="king-block-header king-gray-light">
        <h3 class="king-block-title">填写个人信息</h3>
      </div>

      <div class="king-block-content">
        <table class="table table-bordered table7_demo">
          <thead>
          <tr>
            <th>IP</th>
            <th>机器名</th>
            <th>大区 ID</th>
            <th>大区名</th>
            <th>模块 ID</th>
            <th>模块名</th>
            <th>操作</th>
          </tr>
          </thead>
          <tbody id="tr_data">
            %for host in host_list:
              <tr>
                <th style="width: 15%;">${host['InnerIP']}</th>
                <th style="width: 15%;">${host['OSName']}</th>
                <th style="width: 15%;">${host['CompanyID']}</th>
                <th style="width: 15%;">${host['Region']}</th>
                <th style="width: 15%;">${host['Source']}</th>
                <th style="width: 15%;">${host['DeviceClass']}</th>
                <th>
                  <button class="btn btn-primary" name="execute_task" value=${host['InnerIP']}
                      onclick="execute_task('${host['InnerIP']}')">
                    执行任务
                  </button>
                </th>
              </tr>
            %endfor


          </tbody>
        </table>
      </div>

    </div>
  </div>


  </div>

</%block>

<script type="text/javascript">

  $(document).ready(function () {
    $('#business_select').select2()
    $('#select_task').select2()
  })

  function select_job() {
    var app_data = $("#business_select").val().split('~')
    var app_id = app_data[0]
    var host_html = ''
    var task_html = ''
    $.ajax({
      url: site_url+'get_host_by_app/' + app_id + '/',
      type: 'GET',
      success: function (data) {
        const hosts = data.host_list
        for (var i = 0; i < hosts.length; i++) {
          var html0 =
              "<tr><th >" + hosts[i].InnerIP + "</th>" +
              "<th >" + hosts[i].OSName + "</th>" +
              "<th >" + hosts[i].CompanyID + "</th>" +
              "<th >" + hosts[i].Region + "</th>" +
              "<th >" + hosts[i].Source + "</th>" +
              "<th >" + hosts[i].DeviceClass + "</th>" +
              "<th><button class=\"btn btn-primary\" value=" + hosts[i].InnerIP + " onclick=\"execute_task('" + hosts[i].InnerIP + "')\" >执行任务</button></th></tr>"
          host_html += html0
        }
        $("#tr_data").html(host_html)
      }
    })


    $.ajax({
      url: site_url+'get_task_by_app/' + app_id + '/',
      type: 'GET',
      success: function (data) {
        const tasks = data.task_list
        for (var i = 0; i < tasks.length; i++) {
          var html1 = "<option value=" + tasks[i].id + "~" + tasks[i].name + ">" + tasks[i].name + "</option>"
          task_html += html1
        }
        $("#select_task").html(task_html)
      }
    })

  }

  function execute_task(ip) {
    var task_data = $("#select_task").val().split('~')
    if(task_data[0]===""){
        alert('Please select a task!')
        return
    }
    var task_id = task_data[0]
    var task_name = task_data[1]
    var app_data = $("#business_select").val().split('~');
    var app_id = app_data[0]
    var app_name = app_data[1]

    var d = dialog({
            width: 440,
            title: "提示",
            content: '<div class="king-notice3 king-notice-success">' +
            '        <img src="https://magicbox.bk.tencent.com/static_api/v3/components/loading2/gif/reload_36.gif" all="loading" style="width: 50px;padding-bottom: 20px;">' +
            '<div class="king-notice-text">' +
            '<p class="f24">执行中</p>' +
            '<p class="f12">' +
            '</div>' +
            '</div>',
          });
    d.show();
    $.ajax({
      url: site_url+'execute_task/',
      type: 'POST',
      data: {'ip': ip, 'task_id': task_id, 'task_name': task_name, 'app_id': app_id, 'app_name': app_name},
      success: function (data) {
        result = data.execute_result.result
        if (result) {
          var d = dialog({
            width: 440,
            title: "提示",
            content: '<div class="king-notice3 king-notice-success">' +
            '<span class="king-notice-img"></span>' +
            '<div class="king-notice-text">' +
            '<p class="f24">执行成功</p>' +
            '<p class="f12">' +
            '<span class="king-notice3-color">2秒</span>后跳转至执行历史页面</p>' +
            '</div>' +
            '</div>',
          });
          setTimeout(function () {
            window.location.href = site_url+"history/"
          }, 2000)
        } else {

          var d = dialog({
            width: 440,
            title: "提示",
            content: '<div class="king-notice3 king-notice-fail">' +
            '<span class="king-notice-img"></span>' +
            '<div class="king-notice-text">' +
            '<p class="f24">创建失败</p>' +
            '<p class="f12">' +
            '<span class="king-notice3-color">错误</spa>' + result['message'] +
            '</p>' +
            '</div>' +
            '</div>',
          });
          d.show();
        }
      }
    })

  }


</script>
