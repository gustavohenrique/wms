function workByProcess(params) {
  var processId = params['process'];
  var stepId = params['id'];
  var processName = params['processName'];

  if (processId > 0) {

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
                'id', 'name', 'current_step', 'desc', 'owner', 'datetime_add', 'datetime_change', 'reject', 'reason_reject', 'status', 'can_upload'
              ]
          }),
          proxy: new Ext.data.HttpProxy({
            url: URL_WORKFLOW_PROCESS_WORK+'?process='+processId+'&step='+stepId,
            method: 'POST'
          })
      });
      var grid = new Ext.grid.GridPanel({
          id: 'gridWorkProcess'+processId,
          frame: false,
          border: true,
          title: 'Trabalhos em outros passos ou finalizados',
          //collapsible: true,
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
              { header: 'Passo Atual', dataIndex: 'current_step' },
              { header: 'Dono', dataIndex: 'owner', sortable: true },
              { header: 'Cadastro', dataIndex: 'datetime_add' },
              { header: 'Atualizado', dataIndex: 'datetime_change' },
              { header: 'Recusado', dataIndex: 'reject', width: 70 },
              { header: 'Status', dataIndex: 'status', width: 70 },
              { header: 'Anexos?', dataIndex: 'can_upload', xtype: 'booleancolumn', hidden: true }
            ],
          }),
          sm: new Ext.grid.RowSelectionModel({
              singleSelect: true,
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
                } else alert('Selecione um item');

              }
          }, {
              text: 'Arquivos',
              iconCls: 'attach-icon',
              cls:'x-btn-text-icon',
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
                  } else alert('Selecione um item');
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
                } else alert('Selecione um item');
              }
            },  {
              text: 'Cliente',
              iconCls: 'client-icon',
              cls:'x-btn-text-icon',
              handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                  var sel = sm.getSelected();
                  var id = sel.data.id;
                  if (id > 0) {
                    params = {'workId': id, 'title': sel.data.name};
                    showClientWorkWindow(params, 'accept');
                  }
                } else alert('Selecione um item');
              }
            },  {
              text: 'Produtos',
              iconCls: 'product-icon',
              cls:'x-btn-text-icon',
              handler: function() {
                var sm = grid.getSelectionModel();
                if (sm.hasSelection()) {
                  var sel = sm.getSelected();
                  var id = sel.data.id;
                  if (id > 0) {
                    // Cria uma janela com historico do trabalho
                    params = {'workId': id, 'title': sel.data.name, 'disableEdit': true};
                    showkItemWindow(params);
                  }
                } else alert('Selecione um item');
              }
            }],
            bbar: new Ext.PagingToolbar({
              pageSize: 25,
              store: store,
              displayInfo: true,
              beforePageText: 'Página ',
              afterPageText: ' de {0}',
              displayMsg: 'Exibindo {0} - {1} de {2}',
              emptyMsg: "Nenhum resultado",
            }),
    });
    grid.getView().getRowClass = function(record, index) {
        if (record.data.status == 'Fechado') return 'gray-row';
    };


    if (! Ext.get('gridWorkProcess'+processId)) {
      Ext.getCmp('tbSouth').add({
        id: 'tabWorkProcess'+processId,
        title: processName,
        closable: true,
        layout: 'fit',
        items: [ grid ],
      }).show();
    } else {
        store.load();
        Ext.getCmp('tbSouth').activate('tabWorkProcess'+processId);
    }

  }
}
