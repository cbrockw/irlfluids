#include "fluidsgui.h"
#include "ui_fluidsgui.h"


fluidsgui::fluidsgui(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::fluidsgui)
{
    ui->setupUi(this);
}

fluidsgui::~fluidsgui()
{
    delete ui;
}
