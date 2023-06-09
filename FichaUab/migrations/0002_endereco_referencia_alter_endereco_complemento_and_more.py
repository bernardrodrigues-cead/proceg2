# Generated by Django 4.1.7 on 2023-03-24 16:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('FichaUab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='endereco',
            name='referencia',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='complemento',
            field=models.CharField(blank=True, max_length=31, null=True),
        ),
        migrations.AlterField(
            model_name='mantenedor',
            name='endereco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FichaUab.endereco'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='polo',
            name='endereco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FichaUab.endereco'),
        ),
        migrations.CreateModel(
            name='PessoaFichaUab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bolsa_requerida', models.CharField(choices=[('COORDENADOR UAB I', 'COORDENADOR UAB I'), ('COORDENADOR ADJUNTO UAB I', 'COORDENADOR ADJUNTO UAB I'), ('COORDENADOR DE TUTORIA I', 'COORDENADOR DE TUTORIA I'), ('PROFESSOR REVISOR I', 'PROFESSOR REVISOR I'), ('PROFESSOR REVISOR II', 'PROFESSOR REVISOR II'), ('TUTOR A DISTÂNCIA', 'TUTOR A DISTÂNCIA'), ('PROFESSOR FORMADOR I', 'PROFESSOR FORMADOR I'), ('PROFESSOR FORMADOR II', 'PROFESSOR FORMADOR II'), ('PROFESSOR CONTEUDISTA I', 'PROFESSOR CONTEUDISTA I'), ('PROFESSOR CONTEUDISTA II', 'PROFESSOR CONTEUDISTA II'), ('COORDENADOR DE CURSO I', 'COORDENADOR DE CURSO I'), ('ASSISTENTE À DOCÊNCIA', 'ASSISTENTE À DOCÊNCIA'), ('TUTOR PRESENCIAL', 'TUTOR PRESENCIAL')], max_length=31)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('profissao', models.CharField(max_length=127)),
                ('tipo_documento', models.CharField(choices=[('RG', 'RG'), ('CNH', 'CNH')], max_length=3)),
                ('numero_documento', models.CharField(max_length=31)),
                ('orgao_expeditor', models.CharField(max_length=15)),
                ('data_emissao', models.DateField()),
                ('uf_nascimento', models.CharField(max_length=2)),
                ('municipio_nascimento', models.CharField(max_length=255)),
                ('estado_civil', models.CharField(choices=[('Solteiro(a)', 'Solteiro(a)'), ('Casado(a)', 'Casado(a)'), ('Separado(a)', 'Separado(a)'), ('Divorciado(a)', 'Divorciado(a)'), ('Viúvo(a)', 'Viúvo(a)'), ('União Estável', 'União Estável')], max_length=15)),
                ('nome_conjuge', models.CharField(blank=True, max_length=255, null=True)),
                ('nome_pai', models.CharField(blank=True, max_length=255, null=True)),
                ('nome_mae', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=15)),
                ('area_ultimo_curso_superior', models.CharField(choices=[('Exatas', 'Exatas'), ('Biológicas', 'Biológicas'), ('Humanas', 'Humanas')], max_length=10)),
                ('ultimo_curso_titulacao', models.CharField(max_length=127)),
                ('instituicao_titulacao', models.CharField(max_length=127)),
                ('data_inicio_vinculacao', models.DateField()),
                ('curso_vinculado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FichaUab.curso')),
                ('dados_bancarios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FichaUab.dadosbancarios')),
                ('endereco', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FichaUab.endereco')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FichaUab.pessoa')),
            ],
        ),
    ]
