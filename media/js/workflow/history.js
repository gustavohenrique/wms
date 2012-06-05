
function showHistoryWindow(params) {
  // stepId used only to reload the grid
  workId = params['workId'];

  if (! Ext.get('winHistory'+workId)) {

      var storeFile = new Ext.data.Store({
        autoLoad: true,
        reader: new Ext.data.JsonReader({
          totalProperty: 'total',
          root: 'rows',
          id: 'id',
          fields: [
            'datetime_add', 'user', 'desc'
          ]
        }),
        proxy: new Ext.data.HttpProxy({
          url: URL_WORKFLOW_WORK_HISTORY+'?work='+workId,
          method: 'POST'
        })
      });

      var gridHistory = new Ext.grid.GridPanel({
        id: 'gridHistory'+workId,
        stripeRows: true,
        store: storeFile,
        frame: false,
        border: false,
        autoWidth: true,
        colModel: new Ext.grid.ColumnModel({
          defaults: {
            sortable: false,
            autoWidth: false,
            autoExpandColumn: 'desc',
            editable: false,
            menuDisabled: true
          },
          columns: [
            //new Ext.grid.RowNumberer({width: 30}),
            { header: 'Data e Hora', dataIndex: 'datetime_add', width: 110 },
            { header: 'Usuário', dataIndex: 'user', width: 90 },
            { header: 'Descrição', dataIndex: 'desc', width: 300 },
          ],
        }),
      });

      var w = new Ext.Window({
          title: 'Histórico  ['+params['title']+']',
          id: 'winHistory'+workId,
          width: 400,
          height: 250,
          border: false,
          layout: 'fit',
          items: [ gridHistory ],
        }).show();

  }
}
