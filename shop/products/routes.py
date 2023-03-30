from flask import render_template,session, request,redirect,url_for,flash,current_app,send_from_directory
from shop import app,db, photos
from .models import Category,Brand,Addproduct
from .forms import Addproducts
import secrets, os

def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
        categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
        return categories


@app.route('/')
def landing_page():
    return render_template('products/landing_page.html')

@app.route('/index')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=3)
    return render_template('products/index.html', products=products, brands=brands(), categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product,brands=brands(), categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand = get_b).paginate(page=page, per_page=3)
    return render_template('products/index.html', brand=brand, brands=brands(), categories=categories(), get_b=get_b)



@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category = get_cat).paginate(page=page, per_page=3)
    return render_template('products/index.html', get_cat_prod = get_cat_prod, categories=categories(), brands=brands(), get_cat=get_cat)


@app.route("/addbrand", methods = ["GET", "POST"])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get("brand")
        brand = Brand(name = getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title ='Add Brand', brands = 'brands')


@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/updatebrand.html', title = 'Update Brand Page', updatebrand=updatebrand )


@app.route('/deletebrand/ <int:id>', methods =['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        flash(f'The brand {brand.name} was deleted from your Database','success')
        db.session.commit()
        return redirect(url_for('brands'))
    flash(f'The brand {brand.name} can not be deleted your Database','warning')
    return redirect(url_for('admin'))                                                


@app.route("/addcategory", methods = ["GET", "POST"])
def addcategory():
    if request.method == "POST":
        getcategory = request.form.get("category")
        category = Category(name = getcategory)
        db.session.add(category)
        flash(f'The Category {getcategory} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcategory'))
    return render_template('products/addbrand.html', title = 'Add category')



@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecategory.name = category
        flash(f'The category {updatecategory.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecategory.name
    return render_template('products/updatebrand.html', title = 'Update Category Page', updatecategory=updatecategory )


@app.route('/deletecategory/ <int:id>', methods =['GET', 'POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        flash(f'The Category {category.name} was deleted from your Database','success')
        db.session.commit()
        return redirect(url_for('categories'))
    flash(f'The brand {category.name} can not be deleted your Database','warning')
    return redirect(url_for('admin'))       


@app.route('/addproduct', methods = ['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
        addproduct = Addproduct(name=name, price=price, desc=desc, colors=colors,stock=stock , discount=discount,brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addproduct)
        db.session.commit()
        flash(f'The Product {name} has been added to your Database','success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form = form, title = 'Add a Product', brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods = ['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.description.data
        product.colors = form.colors.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
                
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
                
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")

        flash(f'Your product has been updated' ,'Success')

        db.session.commit()
        return redirect('/admin')
    
    
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.desc
    form.colors.data = product.colors
    brand = product.brand.name
    category = product.category.name
    return render_template('products/updateproduct.html', form = form, title = 'Update Product' ,brands=brands, categories=categories, product=product)



@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('adim'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))
    
    
