""" Basic blog using webpy 0.3 """
import web
import model


urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
)


t_globals = {
    'datestr': web.datestr
}

render=web.template.render('templates', base='base', globals=t_globals)

web.config.debug=False


class Index:

    def GET(self):
        """ mostrar la pagina """
        posts = model.get_posts()
        return render.index(posts)

 
class View:

    def GET(self, id):
        """ Ver un producto """
        post = model.get_post(int(id))
        return render.view(post)


class New:

    form = web.form.Form(
        web.form.Textbox('producto', web.form.notnull, 
            description="producto:"),
        web.form.Textbox('descripcion', web.form.notnull, 
            description="descripcion:"),
        web.form.Textbox('existencias', web.form.notnull, 
            description="existencias:"),
        web.form.Textbox('precio_compra', web.form.notnull, 
            description="precio_compra:"),
        web.form.Textbox('precio_venta', web.form.notnull, 
            description="precio_venta:"),
        web.form.File('imagen_producto', web.form.notnull, 
            description="imagen_producto:"),
        web.form.Button('Enviar'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = web.input()

        form = self.form()

        imagen=web.input(imagen_producto={})
        filedir='static/images'
        filepath=imagen.imagen_producto.filename.replace('\\','/')
        filename=filepath.split('/')[-1]
        
        fout = open(filedir +'/'+ filename, 'w')
        fout.write(imagen.imagen_producto.file.read())
        fout.close()
        imagen_producto = filename
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.producto, form.d.descripcion, form.d.existencias, form.d.precio_compra, form.d.precio_venta, form.d.imagen_producto)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        id_producto=int(id)
        model.del_post(id_producto)
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        id_producto=int(id)
        post = model.get_post(id_producto)
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        id_producto=int(id)
        form = New.form()
        post = model.get_post(id_producto)
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.producto, form.d.descripcion, form.d.existencias, form.d.precio_compra, form.d.precio_venta, form.d.imagen_producto)
        raise web.seeother('/')

app = web.application(urls, globals())


if __name__ == '__main__':
     app.run()