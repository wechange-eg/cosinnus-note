from rest_framework import serializers

from cosinnus_note.models import Note


class NoteListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.URLField(source='get_absolute_url', read_only=True)
    timestamp = serializers.DateTimeField(source='last_modified')

    class Meta(object):
        model = Note
        fields = ('id', 'title', 'text', 'video', 'timestamp')


class NoteRetrieveSerializer(NoteListSerializer):
    pass
