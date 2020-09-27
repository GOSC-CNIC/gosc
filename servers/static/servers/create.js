;'use strict';
(function () {
    let IMAGES = {};    // 缓存镜像信息
    let NETWORKS = {};    // 缓存网络信息
    let FLAVORS = {};    // 缓存网络信息

    function get_image_from_cache(index){
        if (IMAGES.hasOwnProperty(index)){
            return IMAGES[index];
        }
        return null;
    }
    function set_image_to_cache(index, html){
        IMAGES[index] = html;
    }

    function get_network_from_cache(index){
        if (NETWORKS.hasOwnProperty(index)){
            return NETWORKS[index];
        }
        return null;
    }
    function set_network_to_cache(index, html){
        NETWORKS[index] = html;
    }

    function get_flavor_from_cache(index){
        if (FLAVORS.hasOwnProperty(index)){
            return FLAVORS[index];
        }
        return null;
    }
    function set_flavor_to_cache(index, html){
        FLAVORS[index] = html;
    }

    //
    // 页面刷新时执行
    window.onload = function() {
        update_select();
    };

    /*
     * 拼接params对象为url参数字符串
     * @param {Object} obj - 待拼接的对象
     * @returns {string} - 拼接成的query参数字符串
     */
    function encode_params(obj) {
        const params = [];

        Object.keys(obj).forEach((key) => {
            let value = obj[key];
            // 如果值为undefined我们将其置空
            if (typeof value === 'undefined') {
                value = ''
            }
            // 对于需要编码的文本我们要进行编码
            params.push([key, encodeURIComponent(value)].join('='))
        });

        return params.join('&');
    }

    // 校验创建虚拟机参数
    function valid_vm_create_data(obj){
        if(!obj.service_id || obj.service_id <= 0){
            alert('请选择服务端点');
            return false;
        }
        if (!obj.network_id){
            delete obj.network_id;
        }
        if(!obj.image_id){
            alert('请选择系统镜像');
            return false;
        }
        if(!obj.flavor_id){
            alert('请选择配置');
            return false;
        }
        return true;
    }

    // 创建虚拟机表单提交按钮点击事件
    $('form#id-form-server-create button[type="submit"]').click(function (e) {
        e.preventDefault(); // 兼容标准浏览器

        let form = $('form#id-form-server-create');
        let obj_data = getForm2Obj(form);
        if (!valid_vm_create_data(obj_data)){
            return;
        }
        if(!confirm('确定创建服务器实例？'))
            return;

        let api = build_absolute_url('api/server/');
        let json_data = JSON.stringify(obj_data);
        let btn_submit = $(this);
        btn_submit.addClass('disabled'); //鼠标悬停时，使按钮表现为不可点击状态
        btn_submit.attr('disabled', true);//失能对应按钮
        $.ajax({
            url: api,
            type: 'post',
            data: json_data,
            contentType: 'application/json',
            success: function (data, status, xhr) {
                if (xhr.status === 200){
                    if(confirm('创建成功,是否去服务器列表看看？')){
                        window.location = '/servers/';
                    }
                }else{
                    alert("创建失败！" + data.message);
                }
            },
            error: function (xhr) {
                let msg = '创建主机失败!';
                try{
                    msg = msg + xhr.responseJSON.message;
                }catch (e) {}
                alert(msg);
            },
            complete: function () {
                btn_submit.removeClass('disabled');   //鼠标悬停时，使按钮表现为可点击状态
                btn_submit.attr('disabled', false); //激活对应按钮
            }
        })
    });


    // 加载系统镜像下拉框渲染模板
    function render_image_select_items(data){
        let ret='';
        let t = '<option value="{0}">{1}</option>';
        for(let i=0; i<data.length; i++){
            let s = t.format([data[i]['id'], data[i]['name']]);
            ret = ret.concat(s);
        }
        return ret;
    }

    function image_select_update(){
        let service = $('select[name="service_id"]').val();
        if (!service)
            return;

        let html = get_image_from_cache(service);
        let image_select = $('select[name="image_id"]');
        if (html !== null){
            image_select.html(html);
            return;
        }
        image_select.html('');
        let query_str = encode_params({service_id:service});
        $.ajax({
            url: build_absolute_url('api/image/?'+ query_str),
            type: 'get',
            contentType: 'application/json',
            success: function (data, status, xhr) {
                let html = render_image_select_items(data);
                image_select.html(html);
                set_image_to_cache(service, html);
            },
            error: function (xhr) {
                let msg = '获取镜像数据失败!';
                try{
                    msg = msg + xhr.responseJSON.message;
                }catch (e) {}
                alert(msg);
            }
        });
    }

    // 加载配置下拉框渲染模板
    function render_flavor_select_items(data){
        let ret='';
        let t = '<option value="{0}">vcpus:{1}/ram:{2}MB</option>';
        for(let i=0; i<data.length; i++){
            let s = t.format([data[i]['id'], data[i]['vcpus'], data[i]['ram']]);
            ret = ret.concat(s);
        }
        return ret;
    }

    function flavor_select_update(){
        let service = $('select[name="service_id"]').val();
        if (!service)
            return;

        let flavor_select = $('select[name="flavor_id"]');
        let html = get_flavor_from_cache(service);
        if (html !== null){
            flavor_select.html(html);
            return;
        }

        let query_str = encode_params({service_id:service});
        $.ajax({
            url: build_absolute_url('api/flavor/?'+ query_str),
            type: 'get',
            contentType: 'application/json',
            success: function (data, status, xhr) {
                let html = render_flavor_select_items(data['flavors']);
                flavor_select.html(html);
                set_flavor_to_cache(service, html);
            },
            error: function (xhr) {
                let msg = '获取配置样式数据失败!';
                try{
                    msg = msg + xhr.responseJSON.message;
                }catch (e) {}
                alert(msg);
            }
        });
    }


     // 加载网络下拉框渲染模板
    function render_network_select_items(data){
        let ret='';
        let t = '<option value="{0}">{1}</option>';
        for(let i=0; i<data.length; i++){
            let s = t.format([data[i]['id'], data[i]['name']]);
            ret = ret.concat(s);
        }
        return ret;
    }
    function network_select_update(){
        let service = $('select[name="service_id"]').val();
        if (!service)
            return;

        let html = get_network_from_cache(service);
        let network_select = $('select[name="network_id"]');
        if (html !== null){
            network_select.html(html);
            return;
        }
        network_select.html('');
        let query_str = encode_params({service_id:service});
        $.ajax({
            url: build_absolute_url('api/network/?'+ query_str),
            type: 'get',
            contentType: 'application/json',
            success: function (data, status, xhr) {
                let html = render_network_select_items(data);
                network_select.html(html);
                set_network_to_cache(service, html)
            },
            error: function (xhr) {
                let msg = '获取网络数据失败!';
                try{
                    msg = msg + xhr.responseJSON.message;
                }catch (e) {}
                alert(msg);
            }
        });
    }

    function update_select(){
        image_select_update();
        flavor_select_update();
        network_select_update();
    }

    $("#id-service").change(function (e) {
        e.preventDefault();
        image_select_update();
        network_select_update();
    });
})();

