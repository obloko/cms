// TODO: need a way to get all available field types
var FIELD_TYPES = [
    'TextField',
    'CharField',
    'DateTimeField',
    'BooleanField',
    'FileField',
    'ForeignKey',
];

var FieldKwarg = Backbone.Model.extend({
    // schema is for backbone-forms
    schema: {
        name: 'Text',
        value: 'Text',
    },
});

var Field = Backbone.Model.extend({
    // schema is for backbone-forms
    schema: {
        name: { type: 'Text', validators: ['required'] },
        kind: { type: 'Select', validators: ['required'], options: FIELD_TYPES },
        //kwargs: { type:'Text', validators:[validateJSON] }
    },
    // unsaved: { unloadWindowPrompt: true, },
    initialize: function(){ this.startTracking(); },
    save: function(){ this.restartTracking(); },
});

var FieldList = Backbone.Collection.extend({
    model: Field
});