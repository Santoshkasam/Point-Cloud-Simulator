function [ Hist,Dist ] = HIST( Numb,Dmax,Dtar,LamA,LamB,nCo )

% FUNCTION DESCRIPTION
% HIST generates exponential distributed variables as the inter arrvial
% times of incidence photons for given fluxes. The inter arrival times are
% transformed to arrival times. Arrival times of laser and background 
% photons are merged to get the resulting photon flux at each subpixel. 
% From the arrival times on each subpixel coincidence events are determined.
% Coincidence events are accumulated over Ncyc cycles and stored in
% histogramm with bin width Tbin. Finally the distance is calculated from
% the histogramm unsing a proper algorithm.

% INPUT PARAMETERS
% - Numb: Number of detected events per cycle (0 = no limitation)
% - Dmax: Maximum distance [m]
% - Dtar: Specific target distance [m]
% - LamA: Photon flux of reflected laser pulse [Hz]
% - LamB: Photon flux of background/DCR [Hz]
% - nCo:  Coincidence Depth

% OUTPUT PARAMETERS
% - Hist: Raw data histogramm of detected  events
% - Dist: Calculated distance from histogramm [m]

plot = 0;                       % Enables diagramm plotting
algo = 0;                       % Choose algorithm (0, 1 or 2)
                                % 0: Matched filter
                                % 1: Exponential filter
                                % 2: Mean filter
                                % 3: Maximum detection
                                % 4: Center of gravity
                                % 5: Code correlation filter

TDead = 10e-9;                  % SPAD Dead Time [s]
c = 299792458;                  % Speed of light [m/s]
Ncyc = 400;                     % Number of cycles
Ttof = 2*Dtar/c;                % Time of flight [s]
Tbin = 312.5e-12;               % Bin Size [s]
Tpuls = 5e-9;                   % Puls Length [s](5e-9)
Tcyc = 2*Dmax/c+Tpuls;          % Cycle time for given max distance [s]
N = ceil((Tpuls/Tbin-1)/2);     % Filter Size (2N+1) for mean and median
Nbin = ceil(Tcyc/Tbin)+2*N;     % Number of bins
Nsp = 4;                        % Number of subpixel (4)
Theta = 5e-9;                   % Coincidence time [s] (2)
Est = min(320,Nbin);            % Bins for backgrond estimation
PrEn = 200e-9;                  % SPAD Pre-Enable

if Theta > TDead Theta = TDead; end

% Pulse Coding // Bit width = Pulse width
Code = 1;

if nCo > Nsp
    display('Error: Number of subpixels has to be at least coicidence depth.');
    return;
end

LamA = LamA/Nsp;                % Laser photon flux on each subpixel
LamB = LamB/Nsp;                % Bachground photon flux on each subpixel
    
NumB = ceil(Tcyc*LamB);         % Average number of background photons per cycle
NumA = ceil(Tpuls*LamA);        % Average number of photons per reflected puls

Hist = zeros(size(nCo,2),Nbin); %!create the histogram!

% Simulate for each cycle
for k = 1:Ncyc

    % Simulate the detected events for each subpixel 
    for x = 1:Nsp
        
        % Simulate detected events for each object
        for z = 1:size(LamA,2)
            i = 1; 
            ATAt = -1/LamA(z)*log(rand);
            while 1
                if ATAt(i) > Tpuls*sum(Code(z,:))
                    ATAt(i) = 1;
                    break;
                else
                    i = i + 1;
                    % Create exponential distributed inter arrival times
                    ATAt(i) = ATAt(i-1) - 1/LamA(z)*log(rand);
                end
            end
            
            % Generate Puls Code
            Marks = [];
            for i = 1:size(Code,2)
                if Code(z,i) == 1
                    Marks = [Marks,i];
                end
            end
        
            m = 1;
            for k = 1:size(ATAt,2)
                if ATAt(k) == 1
                    break;
                else
                    ATAt(k) = ATAt(k) + (Marks(ceil(ATAt(k)/Tpuls))-ceil(ATAt(k)/Tpuls))*Tpuls;
                end
            end          
       
            ATAt = ATAt + Ttof(z) + PrEn;
            if z == 1
                ATAx = ATAt;
            else
                if size(ATAt,2) > size(ATAx,2)
                    ATAx = [ATAx,ones(z-1,size(ATAt,2)-size(ATAx,2))];
                elseif size(ATAt,2) < size(ATAx,2)
                    ATAt = [ATAt,ones(1,size(ATAx,2)-size(ATAt,2))];
                end
            ATAx = [ATAx;ATAt];
            end
        end
        
        % Merge arrival times of all objects
        Flag = ones(1,size(LamA,2));
        for i = 1:size(LamA,2)*size(ATAx,2)
            Array = ATAx(1,Flag(1));
            for k = 2:size(LamA,2)
                Array = [Array,ATAx(k,Flag(k))];
            end
            [Value,Index] = min(Array);
            Flag(Index) = Flag(Index)+1;
            if Value < 1
                ATA(i) = Value;
            else
                ATA(i) = 1;
                ATA = ATA(1:i);
                break;
            end
        end
        
        if LamB == 0
            ATB(1) = 1;
        else
            i = 1; 
            ATB(1) = -1/LamB*log(rand);
            while 1
                if ATB(i) > Tcyc + PrEn
                    ATB(i) = 1;
                    break;
                else
                    i = i + 1;
                    % Create exponential distributed inter arrival times
                    ATB(i) = ATB(i-1) - 1/LamB*log(rand);
                end
            end
        end
        
        % Merge arrival times of background and puls return
        if ATA(1) < 1 || ATB(1) < 1
            if ATA(1) < 1 && ATB(1) < 1
                n = 1; m = 1; FlagA = 0; FlagB = 0;
                for i = 1:(size(ATA,2)+size(ATB,2))
                    if ATA(n) < ATB(m) && FlagA == 0
                        AT(i) = ATA(n);
                        if n < size(ATA,2)
                            n = n+1;
                        else
                            FlagA = 1;
                        end
                    elseif FlagB == 0
                        AT(i) = ATB(m);
                        if m < size(ATB,2)
                            m = m+1;
                        else
                            FlagB = 1;
                        end
                    end
                    if FlagA == 1 && FlagB == 1
                        AT = AT(1:i);
                        break;
                    end
                end
            elseif ATA(1) < 1
                AT = ATA;
            else
                AT = ATB;
            end

            % Ignore inter-arrival times below dead time
            Last = -TDead;
            n = 1; ATT = 0;
            for i = 1:size(AT,2)
                if AT(i)-Last > TDead
                    ATT(n) = AT(i);
                    Last = ATT(n);
                    n = n+1;
                end
            end
        else
            ATT = 1;
        end 
        
        % Put arrival times of all subpixel in one array
        if x == 1
            ATTx = ATT;
        else
            if size(ATT,2) > size(ATTx,2)
                ATTx = [ATTx,ones(x-1,size(ATT,2)-size(ATTx,2))];
            elseif size(ATT,2) < size(ATTx,2)
                ATT = [ATT,ones(1,size(ATTx,2)-size(ATT,2))];
            end
            ATTx = [ATTx;ATT];
        end
    end
    ATTx = [ATTx,ones(Nsp,1)];
    
    % Merge arrival times of all subpixels
    Flag = ones(1,Nsp);
    for i = 1:Nsp*size(ATTx,2)
        Array = ATTx(1,Flag(1));
        for k = 2:Nsp
            Array = [Array,ATTx(k,Flag(k))];
        end
        [Value,Index] = min(Array);
        Flag(Index) = Flag(Index)+1;
        if Value < 1
            ATx(i) = Value;
        else
            ATx(i) = 1;
            ATx = ATx(1:i);
            break;
        end
    end
    
    for z = 1:size(nCo,2)
        % In case coincidence is deactivated all events are counted if their inter
        % arrival times are greater than the coincidence time (we assume each
        % events generates a pulse with width equal to the coincidence time and the
        % output of all subpixel are connected by an OR)
        n = 2;
        ATc(1) = 1;
        if nCo(z) == 1
            ATc(1) = ATx(1);
            for i = 2:size(ATx,2)-1
                if ATx(i)-ATx(i-1) > Theta
                    ATc(n) = ATx(i);
                    n = n+1;
                end
            end
        % For an coincidence event time between the first and n-th single events
        % must be shorther than the coincidence time and the time between the n-th
        % and the 0-th event muss be greater tahn the coincidence time (this last
        % condition is to garantuee the output of the concurrence detection circuit
        % to be zero since the last coincidence events)
        elseif nCo(z) > 1 && mod(nCo(z),1) == 0
            if size(ATx,2) > nCo(z)
                if ATx(nCo(z))-ATx(1) < Theta
                    ATc(1) = ATx(nCo(z));
                else
                    n = 1;
                end
                for i = 1+nCo(z):size(ATx,2)
                    if ATx(i)-ATx(i-nCo(z)+1) < Theta && ATx(i)-ATx(i-nCo(z)) > Theta
                        ATc(n) = ATx(i);
                        n = n+1;
                    end
                end
            else
                n = 1;
            end
        else
            display('Error: nCo has to be a natural number.');
        end
        ATc(n) = 1;
        ATc = ATc(1:n);
        
        if ATc(1) < 1 && Numb > 0
            % Count only Numb events per cycle
            i = 1;
            while ATc(i) < PrEn
                i = i + 1;
            end
            ATc = ATc(i:min(i+Numb-1,size(ATc,2)));
        end

        % Fill hsitogramm bins
        if ATc(1) < 1
            for i = 1:size(ATc,2)
                Temp = ceil((ATc(i)-PrEn)/Tbin);
                if Temp > 0 && Temp < size(Hist,2)+1
                    Hist(z,Temp)= Hist(z,Temp)+1;
                end
            end
        end
    end
end

% Histogram data processing
for z = 1:size(nCo,2)
    if algo == 0
        % Step 1: Fixed width mean filtering
        for i = 1:Nbin
            F1Hist(i) = mean(Hist(i:i+min(2*N,Nbin-i)));
        end

        % Step 2: Background estimation and subtraction
        bgnd = -log(1-sum(Hist(1:Est))/Ncyc)/Est/Tbin; %+sum(Hist(1:Est))/Est/Tbin/Ncyc;
        bgnd(bgnd>1e8) = 1e8;
        for i = 1:Nbin
            F2Hist(i) = F1Hist(i)-bgnd*exp(-bgnd*i*Tbin)*Tbin*Ncyc;
        end
        F2Hist(F2Hist<0) = 0;

        % Step 3: Finding maximum and use corresponing raw data section
        [Temp,Index] = max(F2Hist(1:ceil(Dmax/c*2/Tbin)));
        F3Hist = Hist(max(1,Index-2*N):min(Nbin,Index+4*N));

        % Step 4: Puls rate estimation and matched filtering
        if max(1,Index-2*N) > 25
            bgnd = -log(1-sum(Hist(1:max(1,Index-2*N)))/Ncyc)/max(1,Index-2*N)/Tbin;
            bgnd(bgnd>1e8) = 1e8;
        end
        % pulr = -log((exp(-bgnd*max(1,Index-2*N)*Tbin)-sum(F3Hist)/Ncyc)/exp(-bgnd*min(Nbin,Index+4*N)*Tbin))/Tpuls;
        pulr = -(log(1-sum(F3Hist)/Ncyc/exp(-bgnd*max(1,Index-2*N)*Tbin))+bgnd*(min(Nbin,Index+4*N)-max(1,Index-2*N))*Tbin)/Tpuls;
        pulr(pulr<0) = 0;
        for i = 1:size(F3Hist,2)
            Temp = 0;
            % Exponential distribution
            for k = i:i+min(2*N,size(F3Hist,2)-i)
                Temp(k-i+1) = F3Hist(k)*exp(-(pulr+bgnd)*(k-i)*Tbin);
                Norm(k-i+1) = exp(-(pulr+bgnd)*(k-i)*Tbin);
            end
            F4Hist(i) = sum(Temp)/sum(Norm);
        end

        % Step 5: Background subtraction and maximum determination
        for i = 1:size(F4Hist,2)
            F5Hist(i) = F4Hist(i)-bgnd*exp(-bgnd*(i+Index-2*N)*Tbin)*Tbin*Ncyc;
        end
        F5Hist(F5Hist<0) = 0;
        [Temp,TofIndex] = max(F5Hist);
        Dist(z) = (TofIndex+max(1,Index-2*N)-3/2)*Tbin*c/2;

        if plot == 1
            display(bgnd);
            display(pulr);
        end
    elseif algo == 1
        for i = 1:Nbin
            Temp = 0;
            % Exponential distribution
            for k = i:i+min(2*N,Nbin-i)
                Temp(k-i+1) = Hist(k)*exp(-LamA/2*(k-i)*Tbin);
                Norm(k-i+1) = exp(-LamA/2*(k-i)*Tbin);
            end
            F1Hist(i) = sum(Temp)/sum(Norm);
        end
        bgnd = -log(1-(sum(Hist)-1)/Ncyc)*c/2/Dmax;
        for i = 1:Nbin
            F1Hist(i) = F1Hist(i)-bgnd*exp(-bgnd*i*Tbin)*Tbin*Ncyc;
        end
        F1Hist(F1Hist<0) = 0;
        [Temp,TofIndex] = max(F1Hist);
        Dist(z) = TofIndex*Tbin*c/2;
    elseif algo == 2
        for i = 1:Nbin
            % Simple mean filter
            F1Hist(i) = (2*N+1)/(min(i+2*N,Nbin)-i+1)*sum(Hist(i:i+min(2*N,Nbin-i)));
        end
        [Temp,TofIndex] = max(F1Hist(1:Nbin-2*N));
        Dist(z) = TofIndex*Tbin*c/2;
    elseif algo == 3
        [Max1,TofIndex1] = max(Hist);
        Hist(TofIndex1) = 0;
        [Max2,TofIndex2] = max(Hist);
        if Max1 == Max2
            Dist(z) = -1;
        else
            Dist(z) = (TofIndex1-0.5)*Tbin*c/2;
        end
    elseif algo == 4
        sumx = 0;
        for i = 1:Nbin
            sumx = sumx + (Tbin/2+Tbin*(i-1))*Hist(i);
        end
        Dist(z) = sumx/sum(Hist)*c/2;
    elseif algo == 5
        for h = 1:size(Code,1)
            Fil = [];
            for i = 1:ceil(size(Code,2)*Tpuls/Tbin)
                Fil = [Fil,Code(h,ceil(i*Tbin/Tpuls))];
            end
            Fil = Fil/sum(Fil);
            for i = 1:size(Hist,2)-size(Fil,2)
                Tmp = 0;
                for k = 1:size(Fil,2)
                    Tmp = Tmp+Fil(k)*Hist(k+i);
                end
                Temp(i) = Tmp;
            end
            if h == 1
                F1Hist = Temp;
            else
                F1Hist = [F1Hist;Temp];
            end
            [Temp,TofIndex] = max(Temp);
            Dist(h,z) = TofIndex*Tbin*c/2;
        end
        F1Hist = [F1Hist,zeros(size(Code,1),size(Fil,2))];
    end
end

if plot == 1
    for i = 1:size(Hist,2)
        Distx(i) = c/2*(i-0.5)*Tbin;
    end
    lim = Dmax;

    figure(1);
    if algo == 0 || algo == 5
        subplot(3,2,1);
    elseif algo == 2 || algo == 1
        subplot(1,2,1);
    end
    set(stem(Distx,Hist),'Marker','none');
    xlabel('Distance [m]');
    ylabel('Count');
    grid on;
    xlim([0,lim]);
    title('Input Data: Unfiltered Histogram');
    set(gca,'FontSize',16);
    
    if algo == 0 || algo == 1 || algo == 2
        if algo == 0
            subplot(3,2,2);
        elseif algo == 1 || algo == 2
            subplot(1,2,2);
        end
        set(stem(Distx,F1Hist),'Marker','none');
        xlabel('Distance [m]');
        ylabel('Count');
        grid on;
        xlim([0,Dmax]);
        title('Step 1: Fixed Width Mean Filtering');
        set(gca,'FontSize',16);
        
        if algo == 0
            subplot(3,2,3);
            set(stem(Distx,F2Hist),'Marker','none');
            [val,ind] = max(F2Hist(1:ceil(Dmax/c*2/Tbin)));
            hold on;
            h = stem(Distx(ind),val,'ro-','markerfacecolor',[1 0 0]);
            xlabel('Distance [m]');
            ylabel('Count');
            grid on;
            xlim([0,Dmax]);
            title('Step 2: Background Estimation and Subtraction');
            set(gca,'FontSize',16);
            cursorMode = datacursormode(gcf);
            cursorMode.createDatatip(h);
            hold off;

            for i = 1:size(F3Hist,2)
                Distx2(i) = c/2*(i+max(1,Index-2*N)-1.5)*Tbin;
            end

            subplot(3,2,4);
            set(stem(Distx2,F3Hist),'Marker','none');
            xlabel('Distance [m]');
            ylabel('Count');
            grid on;
            title('Step 3: Section of Raw Data Histogram');
            set(gca,'FontSize',16);

            subplot(3,2,5);
            set(stem(Distx2,F4Hist),'Marker','none');
            xlabel('Distance [m]');
            ylabel('Count');
            grid on;
            title('Step 4: Puls Rate Estimation and Matched Filtering');
            set(gca,'FontSize',16);

            subplot(3,2,6);
            set(stem(Distx2,F5Hist),'Marker','none');
            [val,ind] = max(F5Hist);
            hold on;
            h = stem(Distx2(ind),val,'ro-','markerfacecolor',[1 0 0]);
            xlabel('Distance [m]');
            ylabel('Count');
            grid on;
            title('Step 5: Background Subtraction and Maximum Determination');
            set(gca,'FontSize',16);
            cursorMode = datacursormode(gcf);
            cursorMode.createDatatip(h);
            hold off;
        end
    elseif algo == 5
        for i = 1:size(Code,1)
            subplot(3,2,i+2);
            set(stem(Distx,F1Hist(i,:)),'Marker','none');
            xlabel('Distance [m]');
            ylabel('Count');
            grid on;
            xlim([0,Dmax]);
            title(['Filter for Code ',num2str(i)]);
            set(gca,'FontSize',16);
        end
    end
    
    set(findall(gcf,'type','text'),'FontSize',16);
    set(gcf,'Color',[1 1 1]);
end
