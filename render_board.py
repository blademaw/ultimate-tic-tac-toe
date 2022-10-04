""" File to render the board as an image with an optional action-reward dictionary. """

import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pylab as plt
import matplotlib, os, imageio

class RenderBoard:
    def __init__(self):
        pass

    def exp_dim(self, b,r,c):
        return (((b//3)%3) * 3 + r, (b%3)*3 + c)

    def saveGameBoard(self, state, move, path, filename=None, rewardDict=None, fileType='png', end=False):
        big_board = np.zeros((9,9))

        if rewardDict is not None:
            for a, v in rewardDict.items():
                big_board[self.exp_dim(a.square, a.x, a.y)] = v

        for b in range(9):
            for r in range(3):
                for c in range(3):
                    big_board[self.exp_dim(b,r,c)] = float('-inf') if state.board[b][r][c] != 0 else big_board[self.exp_dim(b,r,c)]
        
        for filled_square in np.where(state.squares != 0)[0]:
            x,y = self.exp_dim(filled_square,0,0)
            big_board[x:x+3,y:y+3] = float('-inf')
        
        data = big_board
        norm = matplotlib.colors.Normalize(vmin= -1.0, vmax= 1.0)
        cmap='coolwarm_r'
        gridspec_kw = {"height_ratios":[3,3,3], "width_ratios" : [3,3,3]}
        heatmapkws = dict(square=False, cbar=False, cmap = cmap, linewidths=1.0, vmin= -1.0, vmax= 1.0 )

        fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(9, 9), gridspec_kw=gridspec_kw)

        for b in range(9):
            x,y=self.exp_dim(b,0,0)
            board_x,board_y = ((b//3)%3, b%3)
            sns.heatmap(
                data[x:x+3,y:y+3],
                ax=axes[board_x,board_y], 
                xticklabels=list(range(y+1,y+4)) if board_x == 2 else False, 
                yticklabels=list(range(x+1,x+4)) if board_y == 0 else False,
                center=0,
                **heatmapkws)
            
            # small symbols
            if state.squares[b] in (0,-1,-2):
                for x_loc,y_loc in list(zip(*np.where(np.array(state.board[b]) == 1))):
                    axes[board_x,board_y].text(y_loc + 0.5, x_loc + 0.5, 'X', color='black', size=20, ha='center', va='center')
                for x_loc,y_loc in list(zip(*np.where(np.array(state.board[b]) == 2))):
                    axes[board_x,board_y].text(y_loc + 0.5, x_loc + 0.5, 'O', color='black', size=20, ha='center', va='center')
                if rewardDict is not None:
                    for x_loc,y_loc in list(zip(*np.where(np.array(state.board[b]) == 0))):
                        val = np.round(data[self.exp_dim(b,x_loc,y_loc)],2)
                        if val != float("-inf"):
                            axes[board_x,board_y].text(y_loc + 0.5, x_loc + 0.5, str(val), color='black', size=14, ha='center', va='center')
                

        # big symbols
        for s in np.where(state.squares == 1)[0]:
            axes[(s//3)%3, s%3].text(1 + 0.5, 1 + 0.5, 'X', color='black', size=60, ha='center', va='center')
        for s in np.where(state.squares == 2)[0]:
            axes[(s//3)%3, s%3].text(1 + 0.5, 1 + 0.5, 'O', color='black', size=60, ha='center', va='center')

        # add color bar
        cax = fig.add_axes([.945,0.125,0.03,0.7525])
        sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        fig.colorbar(sm, cax=cax)

        fig.suptitle(f"Move {move}", fontsize=30)
        filename = f"{move}.{fileType}" if filename is None else filename
        plt.savefig(os.path.join(path, filename))

        if end and fileType == 'gif':
            print("Saving GIF replay of game...")
            images = []
            image_names = []
            for agent_id in range(2):
                for filename in os.listdir(os.path.join(path,f"{agent_id}")):
                    image_names.append(os.path.join(path,f"{agent_id}",filename))

            image_names.sort(key=lambda y: int(y.split(os.path.sep)[-1].split('.')[0]))
            for _ in range(4): image_names.append(image_names[-1]) # add 4 extra frames at the end

            images = [imageio.imread(filename) for filename in image_names]
            filename = f"replay.{fileType}"
            imageio.mimsave(os.path.join(path, filename), images, duration=0.6)
        
        plt.cla()
        plt.close() # close plots for memory saving