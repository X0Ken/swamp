import subprocess
import gtk

p = subprocess.Popen(["matchbox-keyboard", "--xid"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

keyboard = gtk.Socket()
pid = p.stdout.readline()
print pid
keyboard.add_id(int(pid))

window = gtk.Window()
window.add(keyboard)

keyboard.show()
window.show()
gtk.main()



