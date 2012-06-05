function newWorkForm(processId, processName) {
    /*form.add({
      "fieldLabel": "Nome",
      "name": "name",
      "fieldHidden": false,
      "value": null,
      "header": "name",
      "allowBlank": false,
      "helpText": "",
      "maxLength": 250,
      "invalidText": "",
      "xtype": "textfield"
    }, {
      "fieldLabel": "Descrição",
      "name": "desc",
      "fieldHidden": false,
      "value": null,
      "header": "desc",
      "allowBlank": true,
      "helpText": "",
      "maxLength": 250,
      "invalidText": "",
      "xtype": "textfield"
    });*/

    if (! Ext.get('winNewWorkForm')) {
        var form = new Ext.FormPanel({
            labelWidth: 100,
            url: URL_WORKFLOW_WORK_ADD+'?process='+processId,
            autoScroll: true,
            frame: false,
            border: false,
            bodyStyle : 'padding:10px;',
            defaults: { anchor: '90%' },
            defaultType: 'textfield',
            buttons: [{
                text: 'Salvar',
                handler: function() {
                    if (form.getForm().isValid())
                        form.getForm().submit({
                          success: function(f,a) {
                              Ext.Msg.alert('Alert', 'Trabalho criado com sucesso.');
                              form.getForm().reset();
                          },
                          failure: function(f,a){
                              Ext.Msg.alert('Error', 'Erro ao cadastrar.<br>Verifique se os campos foram preenchidos corretamente.');
                          }
                        });
                    else
                        Ext.Msg.alert('Error', 'Preencha corretamente o formul&aacute;rio.');
                }
            }]
        });
        Ext.Ajax.request({
            url: URL_WORKFLOW_WORK_NEW+'?process='+processId,
            success: function(r) {
                var j = Ext.decode(r.responseText);
                Ext.each(j, function(data) {
                    form.add(data);
                });
                form.doLayout();
            }
        });
        var winNewWorkForm = new Ext.Window({
            title: 'Novo Trabalho ['+processName+']',
            width: 450,
            height: 300,
            layout: 'fit',
            modal: true,
            items: [ form ],
            listeners: {
                close: function() {
                    // Atualiza o menu, recarregando a qtd de trabalhos abertos
                    Ext.getCmp('treeMenu').root.reload();
                }
            }
        }).show();

    }

}


function showInformationWorkWindow(params) {
    /*
     * Show window about data of all steps of the work
     */
    workId = params['workId'];

    if (! Ext.get('winInformation'+workId)) {
        var w = new Ext.Window({
            title: 'Informações',
            id: 'winInformation'+workId,
            width: 500,
            height: 300,
            border: false,
            layout: 'fit',
            html: '<iframe src="'+URL_WORKFLOW_WORK_INFORMATION+'?work='+workId+'" id="iframeInfo'+workId+'" style="width:100%;height:100%;margin:0px;padding:0px;" scrolling="auto" frameborder="0" hspace="0"></iframe>',
        }).show();
    }
}

function showClientWorkWindow(params) {
    /*
     * Show window about data of work client
     */
    workId = params['workId'];

    if (! Ext.get('winClient'+workId)) {
        var w = new Ext.Window({
            title: 'Cliente',
            id: 'winClient'+workId,
            width: 500,
            height: 300,
            border: false,
            layout: 'fit',
            html: '<iframe src="'+URL_WORKFLOW_WORK_CLIENT+'?work='+workId+'" id="iframeInfo'+workId+'" style="width:100%;height:100%;margin:0px;padding:0px;" scrolling="auto" frameborder="0" hspace="0"></iframe>',
        }).show();
    }
}

function showDecisionWindow(params, decision) {
    // stepId used only to reload the grid
    stepId = params['stepId'];
    workId = params['workId'];
    grid = params['grid'];

    if (! Ext.get('winDecision'+workId)) {
        if (decision == 'accept') {
            url = URL_WORKFLOW_WORK_ACCEPT+'?work='+workId+'&step='+stepId;
            buttonLabel = 'Aceitar';
        } else {
            url = URL_WORKFLOW_WORK_REJECT+'?work='+workId+'&step='+stepId;
            buttonLabel = 'Recusar';
        }

        form = new Ext.FormPanel({
            id: 'formDecision',
            labelWidth: 100,
            url: url,
            height: 250,
            autoScroll: true,
            frame: false,
            border: false,
            bodyStyle : 'padding:10px;',
            defaults: { anchor: '95%', msgTarget: 'qtip'},
            defaultType: 'textfield',
            fileUpload: false,
            buttons: [{
                text: buttonLabel,
                handler: function() {
                    if (form.getForm().isValid())
                        form.getForm().submit({
                            success: function(f, action) {
                                Ext.Msg.alert(action.result.status.toUpperCase(), action.result.msg);
                                if (! action.result.status == 'error')
                                    form.getForm().reset();
                            },
                            failure: function(f, action){
                                Ext.Msg.alert('Error', 'Requisição ajax falhou');
                            }
                        });
                    else
                        Ext.Msg.alert('Error', 'Preencha corretamento o formulário.');
                }
            }]
        });

        if (decision == 'accept')
            Ext.Ajax.request({
                url: URL_WORKFLOW_WORK_FORM_ACCEPT+"?work="+workId,
                success: function(r) {
                    var j = Ext.decode(r.responseText);
                    if (j.status == 'error')
                        Ext.Msg.alert('Error','N&atilde;o foi criado campos para esse passo ou voc&ecirc; n&atilde;o tem permiss&atilde;o.<br>Contate o administrador do sistema.');
                    else {
                        Ext.each(j, function(data) {
                          form.add(data);
                        });
                        form.doLayout();
                    }
                }
            });
        else
            form.add({
                name: 'reason_reject',
                fieldLabel: 'Motivo',
                xtype: 'textarea',
                allowBlank: false,
            });

        var w = new Ext.Window({
            title: buttonLabel+' ['+params['title']+']',
            id: 'winDecision'+workId,
            width: 400,
            height: 250,
            border: false,
            maximizable: true,
            layout: 'fit',
            items: [ form ],
            listeners: {
                close: function() {
                    grid.getStore().reload();
                    // Atualiza o menu, recarregando a qtd de trabalhos abertos
                    Ext.getCmp('treeMenu').root.reload();
                }
            }
        }).show();

    }

    $('.brdatefield').setMask({mask:'99/99/9999'});
}
