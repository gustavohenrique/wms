function deleteFile(id) {
  if (id > 0) {
    Ext.Msg.confirm('Confirm','Tem certeza?', function(btn, action) {
      if (btn == 'yes') {
        Ext.Ajax.request({
          url: URL_WORKFLOW_FILE_DEL+'?attach='+id,
          success: function() {
            Ext.getCmp('gridFile'+workId).getStore().load();
          },
          failure: function(r, action) {
            alert(action.result.msg);
          }
        })
      }
    });
  }
}


function showFileWindow(params) {
  // stepId used only to reload the grid
  workId = params['workId'];
  grid = params['grid'];

  if (! Ext.get('winFile'+workId)) {


    form = new Ext.FormPanel({
        id: 'formFile'+workId,
        labelWidth: 100,
        url: '',
        fileUpload: true,
        frame: false,
        border: false,
        title: 'Anexar Arquivo',
        bodyStyle: 'padding: 10px;',
        defaults: {
            anchor: '95%',
            allowBlank: false,
            msgTarget: 'side'
        },
        items: [{
            xtype: 'fileuploadfield',
            id: 'form-file',
            emptyText: 'Selecione um arquivo',
            fieldLabel: 'Arquivo',
            name: 'filepath',
            buttonText: '',
            buttonCfg: {
                iconCls: 'upload-icon'
            }
        }],
        buttons: [{
            text: 'Anexar',
            handler: function() {
                if(form.getForm().isValid()) {
                  form.getForm().submit({
                      method: 'POST',
                      url: URL_WORKFLOW_FILE_ADD+'?work='+workId,
                      waitMsg: 'Enviando...',
                      waitTitle : 'Aguarde',
                      success: function(f, action) {
                        //alert(action.result.msg);
                        if (action.result.status == 'error')
                          Ext.Msg.alert('Error', action.result.msg);
                        else {
                          storeFile.load();
                          Ext.getCmp('formFile'+workId).getForm().reset();
                          Ext.getCmp('tabFile'+workId).activate(0);
                        }
                      },
                      failure: function(fp, action) {
                        alert(action.result.msg);
                      }

                  });
                }
            }
        }]
    });

    /*
     * Grid
     */
    var storeFile = new Ext.data.Store({
      autoLoad: true,
      reader: new Ext.data.JsonReader({
        totalProperty: 'total',
        root: 'rows',
        id: 'id',
        fields: [
          'id', 'filename', 'delete', 'datetime_change'
        ]
      }),
      proxy: new Ext.data.HttpProxy({
        url: URL_WORKFLOW_FILE_LIST+'?work='+workId,
        method: 'POST'
      })
    });

    var gridFile = new Ext.grid.GridPanel({
      id: 'gridFile'+workId,
      title: 'Arquivos',
      stripeRows: true,
      store: storeFile,
      frame: false,
      border: false,
      autoWidth: true,
      colModel: new Ext.grid.ColumnModel({
        defaults: {
          sortable: false,
          autoWidth: false,
          autoExpandColumn: 'filename',
          editable: false,
          menuDisabled: true
        },
        columns: [
          //new Ext.grid.RowNumberer({width: 30}),
          { header: 'ID', dataIndex: 'id', hidden: true },
          { header: 'Arquivo', dataIndex: 'filename', id: 'name', width: 255 },
          { header: 'Data', dataIndex: 'datetime_change', width: 65 },
          { header: 'Excluir', dataIndex: 'delete', width: 45 },
        ],
      }),
      bbar: new Ext.PagingToolbar({
          pageSize: 25,
          store: storeFile,
          displayInfo: true,
          beforePageText: 'Página ',
          afterPageText: ' de {0}',
          displayMsg: 'Exibindo {0} - {1} de {2}',
          emptyMsg: "Nenhum resultado",
        }),
    });

    var tabFile = new Ext.TabPanel({
        id: 'tabFile'+workId,
        activeTab: 0,
        autoScroll: false,
        border: false,
        frame: false,
        items: [ gridFile, form]
    });

    var w = new Ext.Window({
      title: 'Arquivos  ['+params['title']+']',
      id: 'winFile'+workId,
      width: 400,
      height: 250,
      border: false,
      layout: 'fit',
      items: [ tabFile ],
    }).show();

  }
}
