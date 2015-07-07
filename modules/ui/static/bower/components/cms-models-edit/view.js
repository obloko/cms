// hard-coded, fake schema from Martin
var current_schema = {
    "name" : "Album",
    "app_name" : "album",
    "module" : "modules.album",
    "fields" : [ 
        {
            "name" : "first_name",
            "kind" : "CharField",
            "args" : [],
            "kwargs" : {},
        }, 
        {
            "name" : "date_joined",
            "kind" : "DateTimeField",
            "args" : [],
            "kwargs" : {
                "auto_now_add" : true
            },
        }
    ],
    "relations" : [ 
        {
            "name" : "album",
            "kind" : "ForeignKey",
            "args" : [ 
                "self"
            ],
            "kwargs" : {}
        }
    ],
    "inheritance" : [ 
        "Model"
    ],
    "managers" : [ 
        {
            "name" : "objects",
            "kind" : "Manager",
            "args" : [],
            "kwargs" : {}
        }
    ],
    "metadata" : {
        "managed" : false,
        "verbose_name" : "Album model"
    }
};

$(function(){
    
    var schema_fields;

    function init(){
        _.templateSettings.variable = "o";
        
        var app = new Backbone.Marionette.Application();
        app.addRegions({
          fields_region: '#fields-tab'
        });
        app.addInitializer(function(options){
            var view = new FieldListView({ collection: options.fields });
            app.fields_region.show(view);
        });

        // Dummy data
        schema_fields = new FieldList(_.union(current_schema.fields,current_schema.relations));

        app.start({fields: schema_fields});

        $('.add-field-btn').click(showAddFieldForm);

        //$(document).on('click','.btn-add-kwarg', showAddKwargForm);
    }

    function showAddFieldForm(){
        var field = new Field();
        var bbform = new Backbone.Form({model: field}).render();
        var modal = showFormModal('Add Field', bbform.$el);

        bbform.$el.on('submit', function(e) {
            e.preventDefault();
            var errors = bbform.commit();
            if (!errors){
                schema_fields.add(bbform.model);
                modal.close();
            }
        });
    }

    function validateJSON(s){
        // return nothing if OK
        if (typeof(s) == 'string' && s.trim().length){
            try {
                JSON.parse(s);
            } catch (e){
                return {
                    type: 'json',
                    message: 'JSON ' + String(e)
                };
            }
        }
    }

    function showFormModal(title, body_element){
        var M = Backbone.ModalView.extend({
            title: "<h3>"+title+"</h3>",
            buttons: [
                { className: "btn-default cancel", label: "Cancel", close: true },
                { className: "btn-primary save", label: "Save" }],
            events: {
                "click .modal-footer a.save": "onSave",
                "click .modal-footer a.cancel": "onCancel",
                "hidden.bs.modal": "onHidden"
            },
            postRender: function() {
                // this.$body.append($h4).append($p);
                return this;
            },
            onSave: function(e) {
                e.preventDefault();
                this.$el.find('form').submit();
            },
            onCancel: function(e) {
                
            },
            onHidden: function(e) {
                
            }
        });
        return new M({body: body_element}).render();
    }
    
    
    // Views
    var FieldView = Backbone.Marionette.ItemView.extend({
        // Template config
        template: '#field-row-tmpl', tagName: 'tr', className: 'field-row',
        // This causes view to update when model changes, it doesn't happen automatically
        modelEvents: { "change": "render"},
        // Interaction
        events: {
            'blur .field-name input': 'editFieldName',
            'click .btn-add-kwarg': 'showAddKwargForm',
            'click .btn-edit-kwarg': 'showEditKwargForm',
            'click .btn-delete-field': 'deleteField',
            'click .btn-dupe-field': 'dupeField',
        },
        editFieldName: function editFieldName(e){
            var input = $(e.target);
            var model = this.model;
            model.set('name',input.val());
        },
        showAddKwargForm: function(){
            var field_model = this.model;
            var fk = new FieldKwarg();
            var bbform = new Backbone.Form({model: fk}).render();
            var modal = showFormModal('Add Field Option', bbform.$el);
            bbform.$el.on('submit', function(e) {
                e.preventDefault();
                var errors = bbform.commit();
                if (!errors){
                    // You have to clone existing kwargs object, else Backbone won't detect change on the model!
                    var attrs = _.clone(field_model.get('kwargs') || {});
                    attrs[bbform.model.get('name')] = bbform.model.get('value');
                    field_model.set('kwargs',attrs);
                    modal.close();
                }
            });
        },
        showEditKwargForm: function(e){
            var field_model = this.model;
            var $btn = $(e.target);
            var name = $btn.data('name');
            var value = field_model.get('kwargs')[name];
            var fk = new FieldKwarg({name:name,value:value});
            var bbform = new Backbone.Form({model: fk}).render();
            var modal = showFormModal('Edit Field Option', bbform.$el);
            bbform.$el.on('submit', function(e) {
                e.preventDefault();
                var errors = bbform.commit();
                if (!errors){
                    // You have to clone existing kwargs object, else Backbone won't detect change on the model!
                    var attrs = _.clone(field_model.get('kwargs') || {});
                    var new_name = bbform.model.get('name');
                    if (new_name!=name)
                        delete attrs[name];
                    attrs[new_name] = bbform.model.get('value');
                    field_model.set('kwargs',attrs);
                    modal.close();
                }
            });
        },
        dupeField: function(){
            var m = this.model.clone();
            m.set('name',m.get('name')+'_copy');
            schema_fields.add(m);
        },
        deleteField: function(){
            schema_fields.remove(this.model);
        }
    });

    var FieldListView = Backbone.Marionette.CompositeView.extend({
        tagName: 'table',
        className: "table borderless field-list",
        template: "#field-list-tmpl",
        childView: FieldView,
    });

    init();
});