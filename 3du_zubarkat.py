class Vrchol:
    def __init__(self, x = None, levy = None, pravy = None):
        self.info = x          # uložená hodnota
        self.levy = levy       # levý syn
        self.pravy = pravy     # pravý syn
def is_mirror(root):
    return check_levy_pravy(root.levy, root.pravy)
def check_levy_pravy(levy, pravy):
    if not levy and not pravy:
        return True
    if levy and pravy:
        if levy.info==pravy.info:
            levy_half=check_levy_pravy(levy.levy, pravy.pravy)
            pravy_half=check_levy_pravy(levy.pravy, pravy.levy)
            return levy_half and pravy_half
    return False
tree1=Vrchol()
tree1.levy=Vrchol()
tree1.pravy=Vrchol()
tree1.levy.levy=Vrchol()
tree1.levy.pravy=Vrchol()
tree1.pravy.pravy=Vrchol()
tree1.pravy.levy=Vrchol()
tree1.levy.levy.levy=Vrchol()

print(is_mirror(tree1))
