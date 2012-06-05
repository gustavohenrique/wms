function workByStep(params) {
    var stepId = params['id'];
    var processId = params['processId'];
    var stepName = params['title'];
    var processName = params['processName'];
    var manager = params['manager'];
    var participant = params['participant'];

    /*
     ************* Grid ***************
     */
    var expander = new Ext.ux.grid.RowExpander({
        tpl : new Ext.Template(
          '<p class="rowExpander">&nbsp;<b>&bull; Descrição:</b> {desc}<br>&nbsp;<b>&bull; Motivo rejeição:</b> {reason_reject}</p>'
        )
    });
    var store = new Ext.data.Store({
        autoLoad: true,
        reader: new Ext.data.JsonReader({
            totalProperty: 'total',
            root: 'rows',
            id: 'id',
            fields: [
              'id', 'name', 'desc', 'owner', 'datetime_add', 'datetime_change', 'datetime_limit', 'reject', 'reason_reject', 'status', 'can_upload'
            ]
        }),
        proxy: new Ext.data.HttpProxy({
            url: params['urlGrid'],
            method: 'POST'
        })
    });
    var grid = new Ext.grid.GridPanel({
        id: 'gridWork'+stepId,
        frame: false,
        border: true,
        title: 'Trabalhos aguardando resposta',
        plugins: expander,
        autoExpandColumn: 'name',
        stripeRows: true,
        store: store,

        colModel: new Ext.grid.ColumnModel({
            defaults: {
                width: 120,
                sortable: true,
                autoWidth: true,
                editable: false,
                menuDisabled: true
            },
            columns: [
                expander,
                { header: 'ID', dataIndex: 'id', hidden: false, width: 20 },
                { header: 'Nome', dataIndex: 'name', id: 'name' },
                { header: 'Dono', dataIndex: 'owner', sortable: true },
                { header: 'Cadastro', dataIndex: 'datetime_add' },
                { header: 'Atualizado', dataIndex: 'datetime_change' },
                { header: 'Expira', dataIndex: 'datetime_limit' },
                { header: 'Recusado', dataIndex: 'reject', width: 70}, //, xtype: 'booleancolumn' }
                { header: 'Status', dataIndex: 'status', hidden: true },
                { header: 'Anexos?', dataIndex: 'can_upload', xtype: 'booleancolumn', hidden: true }
            ],
        }),
        /* listeners: {
             rowdblclick: {
               fn: function(g, i, e) {
                 var p, title, id;
                 id = g.getSelectionModel().getSelected().get('id');
                 if (id > 0) {
                   title = g.getSelectionModel().getSelected().get('name');
                   p = {'workId': id, 'stepId': stepId, 'title': title}
                   showDecisionWindow(p);
                 } else
                   Ext.Msg.alert('Error', 'Nenhum item selecionado.');
               }
             }
        }, */
        sm: new Ext.grid.RowSelectionModel({
            singleSelect: true,
        }),
        bbar: new Ext.PagingToolbar({
            pageSize: 25,
            store: store,
            displayInfo: true,
            beforePageText: 'Página ',
            afterPageText: ' de {0}',
            displayMsg: 'Exibindo {0} - {1} de {2}',
            emptyMsg: "Nenhum resultado",
        }),
        tbar: [{
            text: 'Histórico',
            iconCls: 'historic-icon',
            cls:'x-btn-text-icon',
            handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var sel = sm.getSelected();
                    var id = sel.data.id;
                    if (id > 0) {
                        // Cria uma janela com historico do trabalho
                        params = {'workId': id, 'title': sel.data.name};
                        showHistoryWindow(params);
                    }
                } else
                     alert('Selecione um item');
            }
        }, {
            text: 'Arquivos',
            iconCls: 'attach-icon',
            cls:'x-btn-text-icon',
            disabled: participant,
            handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var sel = sm.getSelected();
                    var id = sel.data.id;
                    var canUpload = sel.data.can_upload;
                    if (! canUpload) Ext.Msg.alert('Error', 'O item selecionado não permite anexar arquivos.');
                    if (id > 0 && canUpload == true) {
                        params = {'workId': id, 'title': sel.data.name, 'grid': grid};
                        showFileWindow(params);
                    } else
                        alert('Selecione um item');
                }
            }
        }, {
            text: 'Informações',
            iconCls: 'info-icon',
            cls:'x-btn-text-icon',
            handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var sel = sm.getSelected();
                    var id = sel.data.id;
                    if (id > 0) {
                        params = {'workId': id, 'stepId': stepId, 'title': sel.data.name, 'grid': grid};
                        showInformationWorkWindow(params, 'accept');
                    }
                } else
                    alert('Selecione um item');
            }
        }, {
            text: 'Cliente',
            iconCls: 'client-icon',
            cls:'x-btn-text-icon',
            disabled: participant,
            handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var sel = sm.getSelected();
                    var id = sel.data.id;
                    if (id > 0) {
                        params = {'workId': id, 'title': sel.data.name};
                        showClientWorkWindow(params, 'accept');
                    }
                } else
                    alert('Selecione um item');
            }
        }, {
            text: 'Produtos',
            iconCls: 'product-icon',
            cls:'x-btn-text-icon',
            disabled: participant,
            handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var sel = sm.getSelected();
                    var id = sel.data.id;
                    if (id > 0) {
                        // Cria uma janela com historico do trabalho
                        params = {'workId': id, 'title': sel.data.name};
                        showkItemWindow(params);
                    }
                } else
                    alert('Selecione um item');
            }
        }, {
            xtype: 'tbseparator'
        }, {
            text: 'Aceitar',
            iconCls: 'accept-icon',
            cls:'x-btn-text-icon',
            disabled: participant,
            handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var sel = sm.getSelected();
                    var id = sel.data.id;
                    if (id > 0) {
                        params = {'workId': id, 'stepId': stepId, 'title': sel.data.name, 'grid': grid, 'processId': processId};
                        showDecisionWindow(params, 'accept');
                    }
                } else
                    alert('Selecione um item');
            }
        }, {
            text: 'Recusar',
            iconCls: 'reject-icon',
            cls:'x-btn-text-icon',
            disabled: participant,
            handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                    var sel = sm.getSelected();
                    var id = sel.data.id;
                    if (id > 0) {
                        params = {'workId': id, 'stepId': stepId, 'title': sel.data.name, 'grid': grid, 'processId': processId};
                        showDecisionWindow(params, 'reject');
                    }
                } else
                    alert('Selecione um item');
            }
        }, {
            xtype: 'tbfill'
        }, {
            text: 'Tarefas',
            iconCls: 'tasks-icon',
            cls:'x-btn-text-icon',
            handler: function() {
                Ext.Ajax.request({
                    url: URL_WORKFLOW_STEP_TASKS,
                    success: function(r) {
                        var j = Ext.decode(r.responseText);
                        if (! Ext.getCmp('winTask'+stepId)) {
                            winTask = new Ext.Window({
                                id: 'winTask'+stepId,
                                title: 'Tarefas ['+stepName+'/'+processName+']',
                                width: 300,
                                height: 200,
                                html: '<textarea readonly="true" style="width:100%;height:100%;border:0px;background:white;">'+j.tasks+'</textarea>',
                            }).show();
                        }
                    },
                    failure: function(r) {
                        alert('Error: '+r.statusText);
                    },
                    params: {'step': stepId}
                });
            }
        }]
    });

    grid.getView().getRowClass = function(record, index) {
        if (record.data.status == 'Fechado') return 'gray-row';
        if (record.data.reject == 'Sim') return 'red-row';
        //return (record.data.change<0.7 ? (record.data.change<0.5 ? (record.data.change<0.2 ? 'red-row' : 'green-row') : 'blue-row') : '');
    };


    /*
     ************* Tab ***************
     */
    if (! Ext.get('gridWork'+stepId)) {
        Ext.getCmp('tbMain').add({
            id: 'tabStep'+stepId,
            title: stepName,
            closable: true,
            //layout: 'accordion',
            layout: 'fit',
            items: [ grid ],
        }).show();
    } else
        Ext.getCmp('tbMain').activate('tabStep'+stepId);


}
