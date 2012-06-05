function showkItemWindow(params) {
  // stepId used only to reload the grid
  workId = params['workId'];

  /*
   * disableEdit é usado para desativar botoes Salvar, Adicionar
   * e evitar que um item seja removido
   */
  if (params['disableEdit'])
      disableEdit = params['disableEdit'];
  else
      disableEdit = false;

  if (! Ext.get('winItem'+workId)) {

    var rendererReal = function(v) {
        return Ext.util.Format.usMoney(v).replace('$','R$ ');
    }

    var storeProduct = new Ext.data.Store({
      autoLoad: true,
      reader: new Ext.data.JsonReader({
          totalProperty: 'total',
          root: 'rows',
          id: 'id',
          fields: [ 'id', 'name' ]
      }),
      proxy: new Ext.data.HttpProxy({
          url: URL_WORKFLOW_ITEM_PRODUCTS,
          method: 'POST'
      })
    });

    readerItem = new Ext.data.JsonReader({
          totalProperty: 'total',
          root: 'rows',
          id: 'id',
          fields: [
            { name: 'id', type: 'int' },
            { name: 'product', type: 'int' },
            { name: 'amount', type: 'int' },
            { name: 'price', type: 'float' },
            { name: 'productservice' },
            { name: 'grouping' }
          ]
      });

    var groupStoreItem = new  Ext.data.GroupingStore({
        autoLoad: true,
        reader: readerItem,
        groupField: 'grouping',
        sortInfo: {field: 'product', direction: 'ASC'},
        proxy: new Ext.data.HttpProxy({
            url: URL_WORKFLOW_ITEM_LIST+'?work='+workId,
            method: 'POST'
        })
    });

    /*var storeItem = new Ext.data.Store({
      autoLoad: true,
      reader: readerItem,
      proxy: new Ext.data.HttpProxy({
          url: URL_WORKFLOW_ITEM_LIST+'?work='+workId,
          method: 'POST'
      })
    });*/


    // create reusable renderer
    Ext.util.Format.comboRenderer = function(combo){
        return function(value){
            var record = combo.findRecord(combo.valueField, value);
            return record ? record.get(combo.displayField) : combo.valueNotFoundText;
        }
    };
    var comboProduct = new Ext.form.ComboBox({
        typeAhead: true,
        triggerAction: 'all',
        editable: true,
        allowBlank: false,
        displayField: 'name',
        valueField: 'id',
        hiddenName: 'id',
        mode: 'local',
        listClass: 'x-combo-list-small',
        store: storeProduct
    });

    var comboType = new Ext.form.ComboBox({
        typeAhead: true,
        triggerAction: 'all',
        editable: true,
        mode: 'local',
        listClass: 'x-combo-list-small',
        store: PRODUCT_SERVICE_LIST
    });



    // utilize custom extension for Group Summary
    var summary = new Ext.ux.grid.GroupSummary();

    var grid = new Ext.grid.EditorGridPanel({
      id: 'gridItem'+workId,
      store: groupStoreItem,
      autoExpandColumn: 'product', // column with this id will be expanded
      frame: false,
      clicksToEdit: 1,
      view: new Ext.grid.GroupingView({
          forceFit: true,
          showGroupName: false,
          enableNoGroups: false,
          enableGroupingMenu: false,
          hideGroupedColumn: true
      }),
      plugins: summary,
      colModel: new Ext.grid.ColumnModel({
        defaults: {
          editable: true,
          menuDisabled: true,
        },
        columns: [
          //new Ext.grid.RowNumberer({width: 30}),
          {
            header: '&nbsp;',
            dataIndex: 'id',
            align: 'center',
            width: 40,
            fixed: true,
            editable: false,
            renderer: function() {
              return '<img src="'+Ext.BLANK_IMAGE_URL+'" width="16" height="16" class="delete-abled-icon" style="cursor:pointer;">'
            }
          }, {
            header: 'ID',
            dataIndex: 'id',
            hidden: true,
          }, {
            header: 'Agrupamento',
            dataIndex: 'grouping',
            hidden: true,
          }, {
            header: 'Produto',
            dataIndex: 'product',
            id: 'product',
            width: 180,
            editor: comboProduct,
            renderer: Ext.util.Format.comboRenderer(comboProduct),
            summaryType: 'count',
            hideable: false,
            summaryRenderer: function(v, params, data){
                return ((v === 0 || v > 1) ? v +' itens' : '1 item');
            },

          }, {
            header: 'Qtd',
            dataIndex: 'amount',
            width: 65,
            editor: new Ext.form.NumberField({
              allowBlank: false,
              allowNegative: false,
              minValue: 1,
            }),
            summaryType: 'sum',
            hideable: false,
            summaryRenderer: function(v){
                return v;
            },
          }, {
            header: 'Preço Total',
            dataIndex: 'price',
            renderer: rendererReal,
            editor: new Ext.form.NumberField({
              allowBlank: false,
              allowNegative: false,
            }),
            summaryType: 'sum',
            hideable: false,
            summaryRenderer: function(v){
                return Ext.util.Format.usMoney(v).replace('$','R$ ');
            },
          }, {
            header: 'Serviço',
            dataIndex: 'productservice',
            width: 150,
            editor: comboType,
            renderer: Ext.util.Format.comboRenderer(comboType)
          },
        ],
      }),
      bbar: new Ext.PagingToolbar({
          pageSize: 25,
          store: groupStoreItem,
          displayInfo: true,
          beforePageText: 'Página ',
          afterPageText: ' de {0}',
          displayMsg: 'Exibindo {0} - {1} de {2}',
          emptyMsg: "Nenhum resultado",
      }),
      tbar: [{
        text: 'Adicionar item',
        iconCls: 'add-icon',
        disabled: disableEdit,
        handler : function(){
          // access the Record constructor through the grid's store
          var Item = grid.getStore().recordType;
          var i = new Item({
              id: 0,
              product: '',
              amount: 1,
              price: 0,
              productservice: PRODUCT_SERVICE_LIST[0][0],
              grouping: 'Itens'
          });
          grid.stopEditing();
          grid.getStore().insert(0, i);
          grid.startEditing(0, 0);
        }
      }, {
        xtype: 'tbseparator',
      }, {
        text: 'Salvar tabela',
        iconCls: 'save-icon',
        disabled: disableEdit,
        handler : function() {
            var items = [];
            var exist = false;
            var total = grid.store.data.length;
            var oldItems = grid.store.data;
            grid.store.each(function(record) {
                exist = false;

                for (var x=0; x<total; x++) {
                    if (oldItems[x] == record)
                        exist = true;
                }
                if (! exist)
                    items.push(Ext.encode(record.data));
            });

            Ext.Ajax.request({
               url: URL_WORKFLOW_ITEM_ADD,
               params: {
                   'work': workId,
                   'items': '['+items.toString()+']'
               },
               success: function(r) {
                  var j = Ext.decode(r.responseText);
                  Ext.Msg.alert('Alert', j.msg);
                  if (j.status != 'ok')
                      grid.getStore().reload();
               },
            });
        }
      }, {
        xtype: 'tbseparator',
      }, {
        text: 'Gerar PDF',
        iconCls: 'pdf-icon',
        disabled: disableEdit,
        handler: function() {
            window.open(URL_WORK_PEDIDO_REPORT+"?work="+workId, "pedido", "location=0,status=1,scrollbars=1,width=500,height=400");
        }
      }]
    });
    grid.on({
        cellclick: function(grid, rowIndex, columnIndex, e) {
            if(columnIndex !== 0) return;
            var record = grid.store.getAt(rowIndex);
            var id = record.data.id;
            if (id > 0 && disableEdit == false) {
                Ext.Ajax.request({
                    url: URL_WORKFLOW_ITEM_DEL,
                    params: { 'id': id },
                    success: function(r) {
                        var j = Ext.decode(r.responseText);
                        if (j.status == 'error')
                            Ext.Msg.alert('Alert', j.msg);
                        grid.getStore().reload();
                    },
                });
            } else
                if (disableEdit == false)
                    record.store.remove(record);
        },
        beforeedit: function(grid, record, field, value, row, col, cancel) {
            //console.log('entrando em modo edit');
            storeProduct.load();
        },

    });

    var w = new Ext.Window({
      title: 'Produtos  ['+params['title']+']',
      id: 'winItem'+workId,
      width: 600,
      height: 270,
      border: false,
      layout: 'fit',
      items: [ grid ],
    }).show();

  }

}

