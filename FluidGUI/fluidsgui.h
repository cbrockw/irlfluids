#ifndef FLUIDSGUI_H
#define FLUIDSGUI_H

#include <QMainWindow>

namespace Ui {
class fluidsgui;
}

class fluidsgui : public QMainWindow
{
    Q_OBJECT

public:
    explicit fluidsgui(QWidget *parent = nullptr);
    ~fluidsgui();

private:
    Ui::fluidsgui *ui;
};

#endif // FLUIDSGUI_H
