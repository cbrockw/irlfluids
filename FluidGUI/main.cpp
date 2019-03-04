#include "fluidsgui.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    fluidsgui w;
    w.show();

    return a.exec();
}
